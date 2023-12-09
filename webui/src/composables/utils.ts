

export default function getSrc(filename: string): string {
    const server = 'http://server:28100';
    return `${server}/images/${filename}`;
}