

export default function getSrc(filename: string): string {
    const base = process.env.SERVER_URL
    const server = `http://${base}:28100`;
    
    return `${server}/static/${filename}`;
}