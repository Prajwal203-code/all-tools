export type ToolItem = {
  id: string;
  name: string;
  subtitle: string;
  input: string;
  output: string;
  tags: string[];
  processingSeconds: number;
};

export type ToolCategory = {
  id: string;
  title: string;
  tools: ToolItem[];
};

function t(id: string, name: string, subtitle: string, input: string, output: string, tags: string[], processingSeconds: number): ToolItem {
  return { id, name, subtitle, input, output, tags, processingSeconds };
}

export const TOOL_CATEGORIES: ToolCategory[] = [
  {
    id: 'pdf-docs',
    title: 'PDF & Document Tools',
    tools: [
      t('1', 'PDF → Word Converter', 'Convert PDFs into editable Word documents (.docx).', 'PDF file upload', 'Downloadable Word file', ['pdf', 'word', 'docx'], 12),
      t('2', 'PDF → Excel Converter', 'Extract tables from PDF to structured Excel.', 'PDF upload', 'XLSX/CSV with extracted tables', ['pdf', 'excel', 'tables'], 15),
      t('3', 'Word → PDF Converter', 'Convert Word files to PDF format.', 'DOCX/DOC upload', 'PDF file', ['word', 'pdf'], 8),
      t('4', 'Excel → PDF Converter', 'Convert Excel sheets into formatted PDF.', 'XLSX/CSV files', 'PDF with tables/charts', ['excel', 'pdf'], 10),
      t('5', 'PDF Merger', 'Combine multiple PDFs into one.', 'Multiple PDF uploads', 'Single merged PDF', ['pdf', 'merge'], 6),
      t('6', 'PDF Splitter', 'Split PDF into single pages or selected ranges.', 'PDF upload', 'Individual PDFs per page/range', ['pdf', 'split'], 7),
      t('7', 'PDF Editor', 'Add/remove text, images, pages; annotate PDF.', 'PDF upload', 'Editable PDF for download', ['pdf', 'edit', 'annotate'], 18),
      t('8', 'PDF Compressor', 'Reduce PDF size without visible quality loss.', 'PDF upload', 'Compressed PDF', ['pdf', 'compress'], 9),
      t('9', 'PDF OCR', 'Convert scanned PDFs/images to searchable text.', 'Scanned PDF or image', 'Searchable PDF or extracted text', ['pdf', 'ocr'], 20),
      t('10', 'PDF Form Filler', 'Fill PDF forms in bulk from CSV/Excel.', 'PDF form + CSV/Excel data', 'Filled PDFs ready for download', ['pdf', 'forms'], 14),
      t('11', 'PDF → Image Converter', 'Convert each PDF page into JPG/PNG images.', 'PDF upload', 'JPG/PNG images per page', ['pdf', 'image'], 11),
      t('12', 'Image → PDF Converter', 'Combine multiple images into a single PDF.', 'JPG/PNG images', 'Downloadable PDF', ['image', 'pdf'], 6),
      t('13', 'PDF Watermark Tool', 'Add watermark (text/image) to multiple PDFs.', 'PDFs + watermark', 'Watermarked PDFs', ['pdf', 'watermark'], 7),
      t('14', 'PDF Encrypt/Decrypt', 'Encrypt or decrypt PDF files.', 'PDF upload + password', 'Protected or unprotected PDF', ['pdf', 'security'], 5),
      t('15', 'PDF Metadata Editor', 'View & modify PDF metadata.', 'PDF upload', 'PDF with updated metadata', ['pdf', 'metadata'], 4),
      t('16', 'Table Extractor PDF → Excel/CSV', 'Extract tables from PDFs to Excel/CSV.', 'PDF upload', 'XLSX/CSV', ['pdf', 'tables'], 15),
      t('17', 'PDF Summary Generator', 'Generate key points or summaries from PDF.', 'PDF upload', 'Text summary or PDF report', ['pdf', 'ai', 'summary'], 13),
      t('18', 'PDF Annotation Tool', 'Highlight, comment, and draw on PDFs.', 'PDF upload', 'Annotated PDF', ['pdf', 'annotate'], 12),
      t('19', 'PDF Page Reorder Tool', 'Rearrange PDF pages.', 'PDF upload', 'Reordered PDF', ['pdf', 'pages'], 5),
      t('20', 'PDF Template Generator', 'Create reusable PDF templates for reports/forms.', 'Form input or example file', 'Template PDF', ['pdf', 'template'], 10)
    ]
  },
  {
    id: 'excel-csv',
    title: 'Excel & CSV Tools',
    tools: [
      t('21', 'Excel → CSV Converter', 'Convert Excel files to CSV.', 'XLSX upload', 'CSV file', ['excel', 'csv'], 3),
      t('22', 'CSV → Excel Converter', 'Convert CSV to Excel.', 'CSV upload', 'XLSX file', ['csv', 'excel'], 3),
      t('23', 'Excel Deduplicator', 'Remove duplicate rows/columns.', 'Excel/CSV file', 'Cleaned file', ['excel', 'clean'], 6),
      t('24', 'Excel Cleaner', 'Remove empty cells, standardize formatting.', 'Excel/CSV upload', 'Cleaned file', ['excel', 'format'], 6),
      t('25', 'CSV Validator', 'Check for errors in CSV.', 'CSV upload', 'Validation report', ['csv', 'validate'], 5),
      t('26', 'Bulk CSV → SQL Generator', 'Convert CSV to SQL insert statements.', 'CSV/XLSX upload', 'SQL script', ['csv', 'sql'], 8),
      t('27', 'CSV ↔ JSON Converter', 'Convert CSV to JSON or JSON to CSV.', 'CSV/JSON upload', 'Converted file', ['csv', 'json'], 4),
      t('28', 'Excel/CSV Merger', 'Combine multiple Excel or CSV files into one.', 'Multiple files', 'Merged XLSX/CSV', ['excel', 'csv', 'merge'], 7),
      t('29', 'Excel Pivot Table Generator', 'Generate pivot tables from raw data.', 'Excel/CSV upload', 'Pivot table XLSX', ['excel', 'pivot'], 9),
      t('30', 'Excel Chart Generator', 'Create charts from Excel/CSV data.', 'Excel/CSV', 'Charts or embedded XLSX', ['excel', 'charts'], 9)
    ]
  },
  {
    id: 'image-media',
    title: 'Image & Media Tools',
    tools: [
      t('31', 'Bulk Image Resizer', 'Resize multiple images to specified dimensions.', 'JPG/PNG images', 'ZIP of resized images', ['image', 'resize'], 7),
      t('32', 'Image Compressor', 'Reduce image file size without quality loss.', 'Images upload', 'Compressed images (ZIP)', ['image', 'compress'], 6),
      t('33', 'Image Background Remover', 'Automatically remove image backgrounds.', 'JPG/PNG images', 'Transparent PNG', ['image', 'ai'], 11),
      t('34', 'Meme Generator', 'Add text to images to create memes.', 'Image + text', 'Meme image download', ['image', 'meme'], 4),
      t('35', 'Bulk Watermark Tool', 'Add logos or text to multiple images.', 'Images + watermark', 'Watermarked images (ZIP)', ['image', 'watermark'], 6),
      t('36', 'Social Media Thumbnail Generator', 'Generate ready-to-post thumbnails.', 'Image or template', 'Resized/formatted images', ['image', 'social'], 5),
      t('37', 'Image Format Converter', 'Convert images between JPG, PNG, WebP.', 'Images', 'Converted images (ZIP)', ['image', 'convert'], 4),
      t('38', 'Photo Collage Maker', 'Merge multiple images into a single collage.', 'Multiple images', 'Collage image', ['image', 'collage'], 6),
      t('39', 'Color Palette Extractor', 'Extract dominant colors from images.', 'Image upload', 'Color palette (hex)', ['image', 'colors'], 3),
      t('40', 'AI Image Enhancer', 'Enhance image quality using AI.', 'Image upload', 'Enhanced image', ['image', 'ai'], 14),
      t('41', 'AI Image Caption Generator', 'Generate descriptive captions for images.', 'Image upload', 'Caption text + image', ['image', 'ai'], 9),
      t('42', 'Image OCR → Text', 'Extract text from images.', 'JPG/PNG', 'Text file', ['image', 'ocr'], 8),
      t('43', 'Animated GIF Maker', 'Create GIFs from multiple images.', 'Images', 'Animated GIF', ['gif', 'image'], 7),
      t('44', 'Video → GIF Converter', 'Convert short video clips to GIFs.', 'Video files', 'GIF', ['video', 'gif'], 10),
      t('45', 'Meme Template Generator', 'Predefined meme templates for easy creation.', 'Template + text', 'Meme image', ['meme', 'template'], 4)
    ]
  },
  {
    id: 'website-url',
    title: 'Website & URL Tools',
    tools: [
      t('46', 'URL Summarizer', 'Summarize website content using AI.', 'Website URL', 'Text summary', ['url', 'ai'], 12),
      t('47', 'Keyword Scraper', 'Extract top keywords from any page.', 'URL', 'Keywords + frequency', ['seo', 'keywords'], 7),
      t('48', 'Meta Tag Extractor', 'Extract meta title, description, keywords.', 'URL', 'JSON/table of meta tags', ['seo', 'meta'], 5),
      t('49', 'Broken Link Checker', 'Scan website for dead links.', 'URL', 'Table of broken links', ['seo', 'links'], 14),
      t('50', 'Sitemap Generator', 'Generate XML sitemap from website.', 'URL', 'XML file', ['seo', 'sitemap'], 10),
      t('51', 'Page Speed Analyzer', 'Website performance report.', 'URL', 'PDF/HTML report', ['perf', 'seo'], 18),
      t('52', 'Internal Link Visualizer', 'Map internal links of a website.', 'URL', 'Interactive graph', ['seo', 'links'], 12),
      t('53', 'Social Share Preview', 'Preview how link appears on social media.', 'URL', 'Snippet preview image', ['social', 'opengraph'], 6),
      t('54', 'HTML → PDF Generator', 'Convert webpage HTML to PDF.', 'URL or HTML file', 'PDF file', ['html', 'pdf'], 9),
      t('55', 'Bulk Screenshot Generator', 'Capture screenshots of multiple URLs.', 'List of URLs', 'Screenshots (ZIP)', ['screenshot', 'urls'], 16),
      t('56', 'Robots.txt Validator', 'Check robots.txt rules for accessibility.', 'URL', 'Validation report', ['seo', 'robots'], 4),
      t('57', 'Redirect Checker', 'Track URL redirects.', 'URL list', 'Redirect chain table', ['seo', 'redirects'], 7),
      t('58', 'Competitor Content Analyzer', 'Extract headings, meta, keywords.', 'URL(s)', 'SEO insights CSV', ['seo', 'competitor'], 13),
      t('59', 'Website Text Extractor', 'Extract all visible text from webpage.', 'URL', 'Text file', ['scrape', 'text'], 6),
      t('60', 'Web Archive Generator', 'Capture website as PDF/HTML snapshot.', 'URL', 'PDF/ZIP snapshot', ['snapshot', 'archive'], 12)
    ]
  },
  {
    id: 'seo-marketing',
    title: 'SEO & Marketing Tools',
    tools: [
      t('61', 'Keyword Suggestion Tool', 'Generate relevant keywords based on topic.', 'Keyword or topic input', 'Suggested keywords list', ['seo', 'keywords'], 9),
      t('62', 'Backlink Analyzer', 'Analyze backlinks of a domain.', 'Domain input', 'Backlinks table', ['seo', 'backlinks'], 14),
      t('63', 'Competitor Keyword Gap', 'Compare keywords between two domains.', 'Two domains', 'Overlap/unique keywords', ['seo', 'competitor'], 12),
      t('64', 'SEO Audit Report Generator', 'Generate full SEO audit for a site.', 'Website URL', 'PDF/HTML report', ['seo', 'audit'], 18),
      t('65', 'Meta Description Generator', 'Auto-generate SEO meta descriptions.', 'Title/content of page', 'Meta description suggestions', ['seo', 'ai'], 6),
      t('66', 'Hashtag Generator', 'Generate trending hashtags.', 'Content/topic input', 'Hashtag list', ['social', 'hashtags'], 5),
      t('67', 'Social Post Scheduler', 'Schedule posts to multiple platforms.', 'Post content + platform + time', 'Scheduled posts status', ['social', 'schedule'], 15),
      t('68', 'Email List Extractor', 'Extract emails from URL or file.', 'URL / PDF / CSV / TXT', 'CSV of emails', ['email', 'extract'], 7),
      t('69', 'Email Validator', 'Validate email list for deliverability.', 'CSV/Excel email list', 'Validation results CSV', ['email', 'validate'], 10),
      t('70', 'Bulk URL Meta Tag Analyzer', 'Analyze meta tags for multiple URLs.', 'List of URLs', 'CSV with meta tags', ['seo', 'meta'], 8)
    ]
  },
  {
    id: 'ai-automation',
    title: 'AI & Automation Tools',
    tools: [
      t('71', 'AI Content Summarizer', 'Summarize content using AI.', 'File or URL', 'Text summary/PDF', ['ai', 'summary'], 12),
      t('72', 'AI Content Rewriter', 'Paraphrase text content.', 'Text or file', 'Rewritten text', ['ai', 'rewrite'], 9),
      t('73', 'AI FAQ Generator', 'Generate FAQs from website or doc.', 'URL or file', 'FAQ table', ['ai', 'faq'], 9),
      t('74', 'AI Product Description Generator', 'Generate product descriptions.', 'Product CSV or URL', 'Description CSV/PDF', ['ai', 'product'], 10),
      t('75', 'AI Email Subject Line Generator', 'Suggest engaging subject lines.', 'Email content/topic', 'Suggested subject lines', ['ai', 'email'], 5),
      t('76', 'AI Social Post Optimizer', 'Improve social post content.', 'Text input', 'Optimized text', ['ai', 'social'], 7),
      t('77', 'AI Sentiment Analyzer', 'Analyze sentiment of texts.', 'Text/CSV/URL', 'Sentiment score and chart', ['ai', 'sentiment'], 8),
      t('78', 'AI Competitor Report Generator', 'Generate insights on competitor sites.', 'Competitor URL', 'PDF/CSV report', ['ai', 'competitor'], 15),
      t('79', 'AI Table Extractor', 'Extract tables from PDF/images.', 'PDF/image upload', 'Excel/CSV', ['ai', 'tables'], 12),
      t('80', 'AI Text Translator', 'Translate text/files to languages.', 'Text, PDF, Word, CSV', 'Translated file', ['ai', 'translate'], 11)
    ]
  },
  {
    id: 'dev-code',
    title: 'Developer & Code Tools',
    tools: [
      t('81', 'HTML → PDF Converter', 'Convert HTML files or webpages into PDF.', 'HTML file or URL', 'PDF file', ['html', 'pdf'], 8),
      t('82', 'Markdown → HTML/PDF', 'Convert Markdown (.md) to HTML or PDF.', 'Markdown upload or text', 'HTML or PDF', ['markdown', 'pdf'], 6),
      t('83', 'CSS/JS Minifier & Optimizer', 'Minify and optimize CSS/JS files.', 'CSS/JS files', 'Minified files', ['css', 'js', 'optimize'], 5),
      t('84', 'JSON → CSV/Excel', 'Convert JSON files to Excel/CSV.', 'JSON files', 'Excel/CSV', ['json', 'excel'], 4),
      t('85', 'Bulk API Response Tester', 'Test multiple API endpoints.', 'API URLs', 'Status/latency report', ['api', 'test'], 9),
      t('86', 'URL Parameter Cleaner', 'Remove tracking/query parameters.', 'List of URLs', 'Cleaned URLs CSV', ['url', 'clean'], 3),
      t('87', 'Website Content Downloader', 'Download text/images from a website.', 'URL', 'ZIP with text & images', ['scrape', 'download'], 12),
      t('88', 'Bulk URL Response Checker', 'Check HTTP response codes of URLs.', 'URL list', 'Status codes CSV', ['url', 'status'], 6),
      t('89', 'Structured Data Generator', 'Generate JSON-LD for products/events.', 'Form input', 'JSON-LD code', ['seo', 'json-ld'], 5),
      t('90', 'Multi-Page Screenshot → PDF', 'Capture multiple pages and merge PDF.', 'List of URLs', 'PDF file', ['screenshot', 'pdf'], 14)
    ]
  },
  {
    id: 'productivity',
    title: 'Productivity & Misc Tools',
    tools: [
      t('91', 'Bulk Document Renamer', 'Rename documents with a pattern.', 'Files + renaming pattern', 'Renamed files ZIP', ['files', 'rename'], 4),
      t('92', 'File Format Converter', 'Convert between DOCX↔ODT, XLSX↔ODS, etc.', 'Document files', 'Converted files', ['docs', 'convert'], 7),
      t('93', 'Digital Signature Generator', 'Create reusable digital signature stamps.', 'Draw/upload signature', 'Signature PNG/PDF', ['signature', 'pdf'], 5),
      t('94', 'Certificate Generator', 'Bulk generate certificates from names list.', 'Template + CSV of names', 'ZIP of PDFs', ['certificate', 'pdf'], 8),
      t('95', 'Badge Generator', 'Generate badges for events/teams.', 'CSV + template', 'ZIP of PDFs/images', ['badge', 'pdf'], 7),
      t('96', 'Calendar Generator', 'Generate printable monthly/annual calendars.', 'Year/Month + holidays', 'PDF calendar', ['calendar', 'pdf'], 6),
      t('97', 'QR Code Generator', 'Create QR codes for URL/text/contact.', 'Text or URL', 'PNG/JPG QR code', ['qr', 'code'], 3),
      t('98', 'Random Password Generator', 'Generate secure random passwords.', 'Length, complexity options', 'List of passwords', ['password', 'security'], 2),
      t('99', 'ASCII Art Generator', 'Convert text/images into ASCII art.', 'Text or image', 'ASCII art file', ['ascii', 'art'], 5),
      t('100', 'Template Generator', 'Generate templates for invoices, flyers.', 'CSV/text + design', 'PDF/Doc files', ['template', 'pdf'], 10),
      t('101', 'Markdown Resume Builder', 'Create resumes from Markdown input.', 'Markdown text/file', 'PDF resume', ['resume', 'markdown'], 7),
      t('102', 'Email Template Generator', 'Create reusable HTML email templates.', 'Form text/images', 'HTML email file', ['email', 'template'], 6),
      t('103', 'Bulk Text Replacer in Files', 'Search & replace text in files.', 'Files + search/replace', 'Updated files ZIP', ['files', 'text'], 6),
      t('104', 'File Metadata Editor', 'Edit metadata of PDFs/images/Word.', 'Upload file(s)', 'Updated files', ['metadata', 'files'], 6),
      t('105', 'File Version Tracker', 'Track changes/versions of uploaded files.', 'Multiple versions', 'History + diff report', ['version', 'files'], 11)
    ]
  }
];

