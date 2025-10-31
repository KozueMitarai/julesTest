export interface NewsArticle {
  title: string;
  summary: string;
  url: string;
  thumbnail: string;
  category: 'LLM' | 'ImageGeneration' | 'Efficiency' | 'Featured';
}

export const news: NewsArticle[] = [
  {
    title: '【LLM】大規模言語モデルの最新動向とビジネス活用',
    summary: 'LLMの進化が止まらない。最新の研究成果や、ビジネスシーンでの具体的な活用事例を詳しく解説します。',
    url: 'https://example.com/llm-news-1',
    thumbnail: '/images/llm-thumb-1.webp',
    category: 'LLM',
  },
  {
    title: '【画像生成】高品質な画像を誰でも簡単に作成できる新ツールが登場',
    summary: 'テキストから高品質な画像を生成する新しいAIツールがリリースされました。使い方や作例を紹介します。',
    url: 'https://example.com/image-gen-news-1',
    thumbnail: '/images/image-gen-thumb-1.webp',
    category: 'ImageGeneration',
  },
  {
    title: '【業務効率化】AIを活用して日常業務を自動化する方法',
    summary: '繰り返し作業はAIに任せよう。最新のAIツールを使った業務効率化のアイデアと実践的なテクニックをまとめました。',
    url: 'https://example.com/efficiency-news-1',
    thumbnail: '/images/efficiency-thumb-1.webp',
    category: 'Efficiency',
  },
    {
    title: '【注目】個人開発に革命を。AIコーディング支援ツールの比較',
    summary: 'AIがコーディングを支援してくれる時代に。主要なAIコーディングツールの特徴を比較し、個人開発での最適な使い方を探ります。',
    url: 'https://example.com/featured-news-1',
    thumbnail: '/images/featured-thumb-1.webp',
    category: 'Featured',
  },
];
