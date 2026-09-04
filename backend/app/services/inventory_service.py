from collections import defaultdict
from datetime import date
from app.repositories.inventory_repository import InventoryRepository

class InventoryService:
    def __init__(self, repo: InventoryRepository):
        self.repo = repo

    def _rule(self, rules, branch_id, product_id):
        # Specific product+branch > product > branch > global.
        candidates = [r for r in rules if (r['branch_id'] in (None, branch_id)) and (r['product_id'] in (None, product_id))]
        if not candidates:
            return dict(inventory_days=30, minimum_stock=0, maximum_stock=999999999, near_expiry_days=90, sales_history_days=90)
        candidates.sort(key=lambda r: (r['product_id'] is None, r['branch_id'] is None))
        return candidates[0]

    def _sales_map(self, history_days):
        result={}
        for r in self.repo.sales_daily(history_days):
            result[(r['branch_id'],r['product_id'])] = (r['total_sales'] or 0) / max(r['sales_days'] or history_days, 1)
        return result

    def reorder(self):
        rows=self.repo.inventory_rows(); rules=self.repo.rules()
        history=max([r['sales_history_days'] for r in rules], default=90)
        sales=self._sales_map(history)
        po={(r['branch_id'],r['product_id']):r['pending_po'] for r in self.repo.pending_po()}
        grn={(r['branch_id'],r['product_id']):r['pending_grn'] for r in self.repo.pending_grn()}
        grouped=defaultdict(lambda: {'stock':0,'unit_cost':0,'meta':None})
        for r in rows:
            k=(r['branch_id'],r['product_id']); grouped[k]['stock']+=r['quantity'] or 0; grouped[k]['unit_cost']=r['unit_cost'] or 0; grouped[k]['meta']=r
        out=[]
        for (branch_id,product_id),g in grouped.items():
            m=g['meta']; rule=self._rule(rules,branch_id,product_id); daily=sales.get((branch_id,product_id),0)
            lead=m.get('lead_time_days') or 0; inv_days=rule['inventory_days']; minimum=rule['minimum_stock']; maximum=rule['maximum_stock']
            required=max(minimum, daily*(lead+inv_days)); available=g['stock']+po.get((branch_id,product_id),0)+grn.get((branch_id,product_id),0)
            reorder=max(0, required-available)
            # Cap to max stock when a maximum is configured.
            if maximum > 0: reorder=max(0, min(reorder, max(0, maximum-available)))
            if reorder>0:
                out.append(dict(branch_id=branch_id,branch_name=m['branch_name'],product_id=product_id,product_code=m['product_code'],product_name=m['product_name'],current_stock=round(g['stock'],2),pending_po=round(po.get((branch_id,product_id),0),2),pending_grn=round(grn.get((branch_id,product_id),0),2),average_daily_sales=round(daily,2),lead_time_days=lead,inventory_days=inv_days,minimum_stock=minimum,maximum_stock=maximum,required_stock=round(required,2),available_stock=round(available,2),reorder_quantity=round(reorder,2),estimated_value=round(reorder*g['unit_cost'],2),recommendation='REORDER'))
        return out

    def excess(self):
        rows=self.repo.inventory_rows(); rules=self.repo.rules(); history=max([r['sales_history_days'] for r in rules], default=90); sales=self._sales_map(history)
        grouped=defaultdict(lambda:{'stock':0,'unit_cost':0,'meta':None})
        for r in rows:
            k=(r['branch_id'],r['product_id']); grouped[k]['stock']+=r['quantity'] or 0; grouped[k]['unit_cost']=r['unit_cost'] or 0; grouped[k]['meta']=r
        out=[]
        for (bid,pid),g in grouped.items():
            m=g['meta']; rule=self._rule(rules,bid,pid); excess=max(0,g['stock']-rule['maximum_stock']); daily=sales.get((bid,pid),0)
            if excess>0:
                out.append(dict(branch_id=bid,branch_name=m['branch_name'],product_id=pid,product_code=m['product_code'],product_name=m['product_name'],current_stock=round(g['stock'],2),maximum_stock=rule['maximum_stock'],excess_quantity=round(excess,2),unit_cost=round(g['unit_cost'],2),excess_inventory_value=round(excess*g['unit_cost'],2),average_daily_sales=round(daily,2),days_of_inventory=round(g['stock']/daily,2) if daily else None))
        return out

    def near_expiry(self):
        rows=self.repo.inventory_rows(); rules=self.repo.rules(); today=date.today(); out=[]
        for r in rows:
            rule=self._rule(rules,r['branch_id'],r['product_id']); days=(r['expiry_date']-today).days
            if days <= rule['near_expiry_days'] and r['quantity']>0:
                out.append(dict(branch_id=r['branch_id'],branch_name=r['branch_name'],product_id=r['product_id'],product_code=r['product_code'],product_name=r['product_name'],batch_no=r['batch_no'],expiry_date=r['expiry_date'],quantity=round(r['quantity'],2),unit_cost=round(r['unit_cost'],2),inventory_value=round(r['quantity']*r['unit_cost'],2),days_to_expiry=days))
        return sorted(out,key=lambda x:x['days_to_expiry'])

    def branch_summary(self):
        rows=self.repo.inventory_rows(); d=defaultdict(lambda:{'qty':0,'value':0,'products':set(),'name':''})
        for r in rows:
            x=d[r['branch_id']]; x['name']=r['branch_name']; x['qty']+=r['quantity'] or 0; x['value']+=(r['quantity'] or 0)*(r['unit_cost'] or 0); x['products'].add(r['product_id'])
        return [dict(branch_id=k,branch_name=v['name'],total_quantity=round(v['qty'],2),inventory_value=round(v['value'],2),product_count=len(v['products'])) for k,v in d.items()]

    def dashboard(self):
        reorder=self.reorder(); excess=self.excess(); expiry=self.near_expiry(); branches=self.branch_summary()
        return dict(products_requiring_reorder=len(reorder),reorder_value=round(sum(x['estimated_value'] for x in reorder),2),excess_stock_value=round(sum(x['excess_inventory_value'] for x in excess),2),near_expiry_value=round(sum(x['inventory_value'] for x in expiry),2),near_expiry_items=len(expiry),total_inventory_value=round(sum(x['inventory_value'] for x in branches),2),branches=branches)
