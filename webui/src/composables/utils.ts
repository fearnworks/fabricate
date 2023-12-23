

export default function getSrc(filename: string): string {
    const server = `http://${import.meta.env.VITE_SERVER_URL}:28100`;
    
    return `${server}/static/${filename}`;
}