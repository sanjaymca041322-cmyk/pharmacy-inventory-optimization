const API=import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api';
export async function get(path){const r=await fetch(`${API}${path}`);if(!r.ok)throw new Error(await r.text());return r.json();}
export function exportUrl(report,format='xlsx'){return `${API}/reports/export/${report}?format=${format}`}
