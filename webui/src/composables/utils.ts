

export default function getSrc(filename: string): string {
    const server = 'http://localhost:28100';
    return `${server}/static/${filename}`;
}