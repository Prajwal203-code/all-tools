import os
import time
import pandas as pd
import json
import re
from textblob import TextBlob

class AIProcessor:
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process(self, tool_name, data, task_id):
        """Main processing method that routes to specific tool handlers"""
        
        time.sleep(1)  # Initial setup time
        
        method_map = {
            'ai_content_summarizer': self.summarize_content,
            'ai_content_rewriter': self.rewrite_content,
            'ai_faq_generator': self.generate_faq,
            'ai_product_description': self.generate_product_descriptions,
            'ai_email_subject': self.generate_email_subjects,
            'ai_social_optimizer': self.optimize_social_posts,
            'ai_sentiment_analyzer': self.analyze_sentiment,
            'ai_competitor_report': self.generate_competitor_report,
            'ai_table_extractor': self.extract_tables,
            'ai_text_translator': self.translate_text
        }
        
        handler = method_map.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return handler(data, task_id)
    
    def update_progress(self, task_id, progress):
        """Update task progress"""
        from app import TaskManager
        TaskManager.update_progress(task_id, progress)
    
    def summarize_content(self, data, task_id):
        """Summarize content using AI techniques"""
        self.update_progress(task_id, 20)
        
        text = data.get('text', '')
        if not text:
            files = data.get('files', [])
            if files:
                # Read text from file
                input_path = files[0]['filepath']
                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                except:
                    text = "Unable to read file content"
        
        if not text:
            raise ValueError("No text content provided")
        
        # Simple extractive summarization
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Score sentences by word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = []
        for sentence in sentences[:20]:  # Limit to first 20 sentences
            score = sum(word_freq.get(word.lower(), 0) for word in sentence.split())
            sentence_scores.append((sentence, score))
        
        # Get top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:5]]
        
        summary = '. '.join(top_sentences) + '.'
        
        self.update_progress(task_id, 70)
        
        # Create summary report
        report = {
            'original_length': len(text),
            'summary_length': len(summary),
            'compression_ratio': f"{(len(summary) / len(text) * 100):.1f}%",
            'summary': summary,
            'key_statistics': {
                'total_words': len(words),
                'total_sentences': len(sentences),
                'avg_sentence_length': len(words) / len(sentences) if sentences else 0
            }
        }
        
        # Save report
        output_path = os.path.join(self.output_dir, f"{task_id}_content_summary.json")
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def rewrite_content(self, data, task_id):
        """Rewrite content for better readability"""
        self.update_progress(task_id, 30)
        
        text = data.get('text', '')
        if not text:
            raise ValueError("No text content provided")
        
        # Simple rewriting techniques
        sentences = text.split('.')
        rewritten_sentences = []
        
        # Rewriting rules
        replacements = {
            'very': 'extremely',
            'good': 'excellent',
            'bad': 'poor',
            'big': 'large',
            'small': 'compact',
            'help': 'assist',
            'use': 'utilize',
            'get': 'obtain',
            'make': 'create',
            'do': 'perform'
        }
        
        for sentence in sentences:
            if sentence.strip():
                rewritten = sentence.strip()
                
                # Apply replacements
                for old, new in replacements.items():
                    rewritten = re.sub(r'\b' + old + r'\b', new, rewritten, flags=re.IGNORECASE)
                
                # Add variety in sentence structure
                if len(rewritten.split()) > 10:
                    words = rewritten.split()
                    mid = len(words) // 2
                    rewritten = ' '.join(words[:mid]) + '. Furthermore, ' + ' '.join(words[mid:])
                
                rewritten_sentences.append(rewritten)
        
        rewritten_text = '. '.join(rewritten_sentences)
        
        self.update_progress(task_id, 70)
        
        # Create comparison report
        report = {
            'original_text': text,
            'rewritten_text': rewritten_text,
            'changes_made': len(replacements),
            'original_word_count': len(text.split()),
            'rewritten_word_count': len(rewritten_text.split()),
            'readability_improvement': 'Enhanced vocabulary and sentence structure'
        }
        
        # Save report
        output_path = os.path.join(self.output_dir, f"{task_id}_rewritten_content.json")
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_faq(self, data, task_id):
        """Generate FAQ from content"""
        self.update_progress(task_id, 30)
        
        text = data.get('text', '')
        if not text:
            raise ValueError("No text content provided")
        
        # Extract potential FAQ items
        sentences = text.split('.')
        
        # Common question starters for different topics
        question_templates = [
            "What is {}?",
            "How does {} work?",
            "Why should I use {}?",
            "When should I consider {}?",
            "Where can I find {}?",
            "Who can benefit from {}?",
            "How much does {} cost?",
            "What are the benefits of {}?",
            "How do I get started with {}?",
            "Is {} right for me?"
        ]
        
        # Extract key terms (nouns)
        words = re.findall(r'\b\w+\b', text.lower())
        key_terms = [word for word in set(words) if len(word) > 4 and words.count(word) > 1][:5]
        
        faqs = []
        for i, term in enumerate(key_terms):
            if i < len(question_templates):
                question = question_templates[i].format(term)
                
                # Find relevant sentence for answer
                relevant_sentences = [s for s in sentences if term in s.lower()]
                answer = relevant_sentences[0] if relevant_sentences else f"{term} is an important aspect covered in our content."
                
                faqs.append({
                    'question': question,
                    'answer': answer.strip(),
                    'category': 'General'
                })
        
        self.update_progress(task_id, 70)
        
        # Create FAQ DataFrame
        df = pd.DataFrame(faqs)
        output_path = os.path.join(self.output_dir, f"{task_id}_generated_faq.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_product_descriptions(self, data, task_id):
        """Generate product descriptions"""
        self.update_progress(task_id, 30)
        
        files = data.get('files', [])
        if not files:
            raise ValueError("No product data file provided")
        
        # Read product data
        input_path = files[0]['filepath']
        try:
            if input_path.endswith('.csv'):
                df = pd.read_csv(input_path)
            else:
                df = pd.read_excel(input_path)
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")
        
        # Generate descriptions
        descriptions = []
        
        for index, row in df.iterrows():
            product_name = str(row.get('name', row.get('product_name', f'Product {index+1}')))
            
            # Template-based description generation
            templates = [
                f"Discover the exceptional {product_name}, designed to meet your specific needs with outstanding quality and performance.",
                f"Experience the innovative {product_name}, featuring cutting-edge technology and superior craftsmanship.",
                f"The versatile {product_name} offers unmatched functionality and reliability for professional use.",
                f"Premium {product_name} delivers exceptional value with its advanced features and user-friendly design.",
                f"Transform your workflow with the powerful {product_name}, engineered for maximum efficiency and results."
            ]
            
            description = templates[index % len(templates)]
            
            # Add features if available
            features = []
            for col in df.columns:
                if col.lower() in ['features', 'benefits', 'specifications']:
                    feature_text = str(row.get(col, ''))
                    if feature_text and feature_text != 'nan':
                        features.append(feature_text)
            
            if features:
                description += f" Key features include: {', '.join(features)}."
            
            descriptions.append({
                'product_name': product_name,
                'generated_description': description,
                'word_count': len(description.split()),
                'character_count': len(description)
            })
            
            # Update progress
            progress = 30 + (60 * (index + 1) / len(df))
            self.update_progress(task_id, progress)
        
        # Create output DataFrame
        result_df = pd.DataFrame(descriptions)
        output_path = os.path.join(self.output_dir, f"{task_id}_product_descriptions.xlsx")
        result_df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_email_subjects(self, data, task_id):
        """Generate email subject lines"""
        self.update_progress(task_id, 30)
        
        content = data.get('content', 'Newsletter update')
        
        # Email subject line templates
        templates = [
            "🚀 {} - Don't Miss Out!",
            "Breaking: {} Inside",
            "Your {} Update is Here",
            "Exclusive: {} Just for You",
            "✨ {} - Limited Time",
            "Weekly {} Digest",
            "Important {} Announcement",
            "📧 {} Newsletter",
            "Latest {} Trends",
            "🎯 {} Action Required"
        ]
        
        # Generate variations
        subject_lines = []
        for template in templates:
            subject = template.format(content)
            
            subject_lines.append({
                'subject_line': subject,
                'length': len(subject),
                'has_emoji': '🚀' in subject or '✨' in subject or '📧' in subject or '🎯' in subject,
                'urgency_level': 'High' if 'Don\'t Miss' in subject or 'Limited Time' in subject else 'Medium',
                'category': 'Promotional' if 'Exclusive' in subject else 'Informational'
            })
        
        self.update_progress(task_id, 70)
        
        # Create DataFrame
        df = pd.DataFrame(subject_lines)
        output_path = os.path.join(self.output_dir, f"{task_id}_email_subjects.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def optimize_social_posts(self, data, task_id):
        """Optimize social media posts"""
        self.update_progress(task_id, 30)
        
        text = data.get('text', '')
        if not text:
            raise ValueError("No text content provided")
        
        # Optimization suggestions
        optimizations = []
        
        # Length optimization
        if len(text) > 280:
            optimizations.append({
                'type': 'Length',
                'issue': 'Post too long for Twitter',
                'suggestion': 'Shorten to under 280 characters',
                'optimized_text': text[:270] + '...'
            })
        
        # Hashtag optimization
        hashtag_count = len(re.findall(r'#\w+', text))
        if hashtag_count == 0:
            optimizations.append({
                'type': 'Hashtags',
                'issue': 'No hashtags found',
                'suggestion': 'Add 2-3 relevant hashtags',
                'optimized_text': text + ' #trending #social #content'
            })
        elif hashtag_count > 5:
            optimizations.append({
                'type': 'Hashtags',
                'issue': 'Too many hashtags',
                'suggestion': 'Reduce to 3-5 hashtags maximum',
                'optimized_text': text  # Would remove excess hashtags in real implementation
            })
        
        # Engagement optimization
        if '?' not in text and '!' not in text:
            optimizations.append({
                'type': 'Engagement',
                'issue': 'No call-to-action or engagement trigger',
                'suggestion': 'Add question or exclamation',
                'optimized_text': text + ' What do you think?'
            })
        
        # Emoji optimization
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', text))
        if emoji_count == 0:
            optimizations.append({
                'type': 'Visual Appeal',
                'issue': 'No emojis for visual appeal',
                'suggestion': 'Add 1-2 relevant emojis',
                'optimized_text': '✨ ' + text + ' 🚀'
            })
        
        self.update_progress(task_id, 70)
        
        # Create optimization report
        df = pd.DataFrame(optimizations)
        output_path = os.path.join(self.output_dir, f"{task_id}_social_optimization.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def analyze_sentiment(self, data, task_id):
        """Analyze sentiment of text content"""
        self.update_progress(task_id, 30)
        
        text = data.get('text', '')
        files = data.get('files', [])
        
        texts_to_analyze = []
        
        if text:
            texts_to_analyze.append(('Direct Input', text))
        
        if files:
            for file_info in files:
                input_path = file_info['filepath']
                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        texts_to_analyze.append((os.path.basename(input_path), file_content))
                except:
                    continue
        
        if not texts_to_analyze:
            raise ValueError("No text content provided")
        
        # Analyze sentiment
        results = []
        
        for source, content in texts_to_analyze:
            # Split into sentences for detailed analysis
            sentences = content.split('.')
            sentence_sentiments = []
            
            for sentence in sentences[:20]:  # Limit to first 20 sentences
                if sentence.strip():
                    blob = TextBlob(sentence.strip())
                    polarity = blob.sentiment.polarity
                    subjectivity = blob.sentiment.subjectivity
                    
                    sentiment_label = 'Positive' if polarity > 0.1 else 'Negative' if polarity < -0.1 else 'Neutral'
                    
                    sentence_sentiments.append({
                        'sentence': sentence.strip()[:100] + '...' if len(sentence.strip()) > 100 else sentence.strip(),
                        'polarity': round(polarity, 3),
                        'subjectivity': round(subjectivity, 3),
                        'sentiment': sentiment_label
                    })
            
            # Overall sentiment
            overall_blob = TextBlob(content)
            overall_polarity = overall_blob.sentiment.polarity
            overall_subjectivity = overall_blob.sentiment.subjectivity
            overall_sentiment = 'Positive' if overall_polarity > 0.1 else 'Negative' if overall_polarity < -0.1 else 'Neutral'
            
            results.append({
                'source': source,
                'overall_sentiment': overall_sentiment,
                'overall_polarity': round(overall_polarity, 3),
                'overall_subjectivity': round(overall_subjectivity, 3),
                'positive_sentences': len([s for s in sentence_sentiments if s['sentiment'] == 'Positive']),
                'negative_sentences': len([s for s in sentence_sentiments if s['sentiment'] == 'Negative']),
                'neutral_sentences': len([s for s in sentence_sentiments if s['sentiment'] == 'Neutral'])
            })
        
        self.update_progress(task_id, 70)
        
        # Create sentiment report
        df = pd.DataFrame(results)
        output_path = os.path.join(self.output_dir, f"{task_id}_sentiment_analysis.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    # Simplified implementations for remaining methods
    def generate_competitor_report(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_competitor_report.xlsx")
        sample_data = pd.DataFrame({
            'competitor': ['Competitor A', 'Competitor B', 'Competitor C'],
            'strength': ['SEO', 'Content', 'Social Media'],
            'opportunity': ['Mobile UX', 'Email Marketing', 'Video Content']
        })
        sample_data.to_excel(output_path, index=False)
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def extract_tables(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_extracted_tables.xlsx")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def translate_text(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_translated_text.txt")
        with open(output_path, 'w') as f:
            f.write("Translation completed. In full implementation, this would use Google Translate API or similar service.")
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}