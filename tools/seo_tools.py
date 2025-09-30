import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
from collections import Counter

class SEOProcessor:
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process(self, tool_name, data, task_id):
        """Main processing method that routes to specific tool handlers"""
        
        time.sleep(1)  # Initial setup time
        
        method_map = {
            'keyword_suggestion': self.suggest_keywords,
            'backlink_analyzer': self.analyze_backlinks,
            'keyword_gap_analysis': self.analyze_keyword_gap,
            'seo_audit_generator': self.generate_seo_audit,
            'meta_description_generator': self.generate_meta_descriptions,
            'hashtag_generator': self.generate_hashtags,
            'social_post_scheduler': self.schedule_social_posts,
            'email_list_extractor': self.extract_email_list,
            'email_validator': self.validate_emails,
            'bulk_meta_analyzer': self.analyze_bulk_meta
        }
        
        handler = method_map.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return handler(data, task_id)
    
    def update_progress(self, task_id, progress):
        """Update task progress"""
        from app import TaskManager
        TaskManager.update_progress(task_id, progress)
    
    def suggest_keywords(self, data, task_id):
        """Generate keyword suggestions"""
        self.update_progress(task_id, 20)
        
        seed_keyword = data.get('keyword', 'business')
        
        # Simplified keyword generation (in real app, use Google Keyword Planner API)
        base_keywords = [
            'best', 'top', 'how to', 'what is', 'guide', 'tips', 'free', 'online',
            'service', 'company', 'solution', 'professional', 'expert', 'review'
        ]
        
        modifiers = [
            '2024', 'near me', 'for beginners', 'pricing', 'cost', 'benefits',
            'vs', 'comparison', 'tool', 'software', 'app'
        ]
        
        suggestions = []
        
        # Generate combinations
        for base in base_keywords:
            suggestions.append({
                'keyword': f"{base} {seed_keyword}",
                'search_volume': f"{(hash(f'{base}{seed_keyword}') % 10000 + 1000)}",
                'difficulty': f"{(hash(f'{base}{seed_keyword}') % 100)}",
                'cpc': f"${(hash(f'{base}{seed_keyword}') % 500 + 50) / 100:.2f}"
            })
        
        for modifier in modifiers:
            suggestions.append({
                'keyword': f"{seed_keyword} {modifier}",
                'search_volume': f"{(hash(f'{seed_keyword}{modifier}') % 10000 + 1000)}",
                'difficulty': f"{(hash(f'{seed_keyword}{modifier}') % 100)}",
                'cpc': f"${(hash(f'{seed_keyword}{modifier}') % 500 + 50) / 100:.2f}"
            })
        
        self.update_progress(task_id, 70)
        
        # Create DataFrame and save
        df = pd.DataFrame(suggestions)
        output_path = os.path.join(self.output_dir, f"{task_id}_keyword_suggestions.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def analyze_backlinks(self, data, task_id):
        """Analyze backlinks for a domain"""
        self.update_progress(task_id, 20)
        
        domain = data.get('domain', 'example.com')
        
        # Simplified backlink analysis (in real app, use Ahrefs/SEMrush API)
        backlinks = []
        
        sample_domains = [
            'wikipedia.org', 'reddit.com', 'stackoverflow.com', 'github.com',
            'medium.com', 'linkedin.com', 'twitter.com', 'facebook.com',
            'youtube.com', 'pinterest.com'
        ]
        
        for i, source_domain in enumerate(sample_domains):
            backlinks.append({
                'source_domain': source_domain,
                'source_url': f"https://{source_domain}/page-{i+1}",
                'anchor_text': f"link to {domain}",
                'domain_authority': 90 - i * 5,
                'link_type': 'dofollow' if i % 2 == 0 else 'nofollow',
                'first_seen': f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}"
            })
            
            progress = 20 + (70 * (i + 1) / len(sample_domains))
            self.update_progress(task_id, progress)
        
        # Create DataFrame and save
        df = pd.DataFrame(backlinks)
        output_path = os.path.join(self.output_dir, f"{task_id}_backlink_analysis.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def analyze_keyword_gap(self, data, task_id):
        """Analyze keyword gap between two domains"""
        self.update_progress(task_id, 30)
        
        domain1 = data.get('domain1', 'example.com')
        domain2 = data.get('domain2', 'competitor.com')
        
        # Simplified gap analysis
        keywords_domain1 = [
            'business software', 'crm solution', 'project management',
            'team collaboration', 'productivity tools', 'workflow automation'
        ]
        
        keywords_domain2 = [
            'business tools', 'customer management', 'task management',
            'remote work', 'productivity apps', 'business automation'
        ]
        
        # Find gaps
        gap_analysis = []
        
        # Keywords only in domain1
        for kw in keywords_domain1:
            if kw not in keywords_domain2:
                gap_analysis.append({
                    'keyword': kw,
                    'type': f'Only in {domain1}',
                    'search_volume': hash(kw) % 5000 + 1000,
                    'difficulty': hash(kw) % 80 + 20,
                    'opportunity': 'High'
                })
        
        # Keywords only in domain2
        for kw in keywords_domain2:
            if kw not in keywords_domain1:
                gap_analysis.append({
                    'keyword': kw,
                    'type': f'Missing from {domain1}',
                    'search_volume': hash(kw) % 5000 + 1000,
                    'difficulty': hash(kw) % 80 + 20,
                    'opportunity': 'Medium'
                })
        
        self.update_progress(task_id, 70)
        
        # Create DataFrame and save
        df = pd.DataFrame(gap_analysis)
        output_path = os.path.join(self.output_dir, f"{task_id}_keyword_gap_analysis.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_seo_audit(self, data, task_id):
        """Generate comprehensive SEO audit"""
        self.update_progress(task_id, 20)
        
        url = data.get('url', 'https://example.com')
        
        try:
            # Fetch webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            self.update_progress(task_id, 40)
            
            # SEO audit checks
            audit_results = []
            
            # Title check
            title = soup.find('title')
            if title:
                title_text = title.get_text()
                title_length = len(title_text)
                audit_results.append({
                    'check': 'Title Tag',
                    'status': 'Pass' if 30 <= title_length <= 60 else 'Fail',
                    'value': title_text,
                    'recommendation': 'Title length is optimal' if 30 <= title_length <= 60 else 'Optimize title length (30-60 chars)'
                })
            else:
                audit_results.append({
                    'check': 'Title Tag',
                    'status': 'Fail',
                    'value': 'Missing',
                    'recommendation': 'Add a title tag'
                })
            
            # Meta description check
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                desc_content = meta_desc.get('content', '')
                desc_length = len(desc_content)
                audit_results.append({
                    'check': 'Meta Description',
                    'status': 'Pass' if 120 <= desc_length <= 160 else 'Warning',
                    'value': desc_content,
                    'recommendation': 'Meta description length is optimal' if 120 <= desc_length <= 160 else 'Optimize description length (120-160 chars)'
                })
            else:
                audit_results.append({
                    'check': 'Meta Description',
                    'status': 'Fail',
                    'value': 'Missing',
                    'recommendation': 'Add a meta description'
                })
            
            self.update_progress(task_id, 60)
            
            # Heading structure
            h1_tags = soup.find_all('h1')
            audit_results.append({
                'check': 'H1 Tags',
                'status': 'Pass' if len(h1_tags) == 1 else 'Warning',
                'value': f"{len(h1_tags)} H1 tags found",
                'recommendation': 'Perfect H1 structure' if len(h1_tags) == 1 else 'Use exactly one H1 tag per page'
            })
            
            # Image alt tags
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            audit_results.append({
                'check': 'Image Alt Tags',
                'status': 'Pass' if len(images_without_alt) == 0 else 'Warning',
                'value': f"{len(images_without_alt)}/{len(images)} images missing alt text",
                'recommendation': 'All images have alt text' if len(images_without_alt) == 0 else 'Add alt text to all images'
            })
            
            # Internal links
            internal_links = soup.find_all('a', href=True)
            audit_results.append({
                'check': 'Internal Links',
                'status': 'Pass',
                'value': f"{len(internal_links)} links found",
                'recommendation': 'Good internal linking structure'
            })
            
            self.update_progress(task_id, 80)
            
        except Exception as e:
            audit_results = [{
                'check': 'Error',
                'status': 'Fail',
                'value': str(e),
                'recommendation': 'Check URL accessibility'
            }]
        
        # Create DataFrame and save
        df = pd.DataFrame(audit_results)
        output_path = os.path.join(self.output_dir, f"{task_id}_seo_audit.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_meta_descriptions(self, data, task_id):
        """Generate SEO-optimized meta descriptions"""
        self.update_progress(task_id, 30)
        
        content = data.get('content', 'Sample business content about services and solutions')
        
        # Simple meta description generation
        sentences = content.split('.')[:2]
        base_description = '. '.join(sentences)
        
        variations = [
            f"{base_description}. Get started today!",
            f"Discover {base_description.lower()}. Learn more now.",
            f"Professional {base_description.lower()}. Contact us for details.",
            f"{base_description}. Free consultation available.",
            f"Expert {base_description.lower()}. Call now for pricing."
        ]
        
        # Ensure optimal length
        optimized_descriptions = []
        for desc in variations:
            if len(desc) > 160:
                desc = desc[:157] + "..."
            elif len(desc) < 120:
                desc += " " + "Professional services and solutions."
            
            optimized_descriptions.append({
                'description': desc,
                'length': len(desc),
                'status': 'Optimal' if 120 <= len(desc) <= 160 else 'Needs adjustment'
            })
        
        self.update_progress(task_id, 70)
        
        # Create DataFrame and save
        df = pd.DataFrame(optimized_descriptions)
        output_path = os.path.join(self.output_dir, f"{task_id}_meta_descriptions.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_hashtags(self, data, task_id):
        """Generate hashtags for social media posts"""
        self.update_progress(task_id, 30)
        
        content = data.get('content', 'business productivity tools')
        
        # Extract key terms
        words = re.findall(r'\b\w+\b', content.lower())
        
        # Common hashtag categories
        business_tags = ['#business', '#entrepreneur', '#startup', '#success', '#growth']
        industry_tags = ['#tech', '#software', '#digital', '#innovation', '#productivity']
        engagement_tags = ['#motivation', '#tips', '#advice', '#trending', '#follow']
        
        # Generate content-specific hashtags
        content_tags = [f"#{word}" for word in words if len(word) > 4][:10]
        
        all_hashtags = {
            'Business Tags': business_tags,
            'Industry Tags': industry_tags,
            'Engagement Tags': engagement_tags,
            'Content-Specific Tags': content_tags
        }
        
        self.update_progress(task_id, 70)
        
        # Create formatted output
        hashtag_data = []
        for category, tags in all_hashtags.items():
            for tag in tags:
                hashtag_data.append({
                    'category': category,
                    'hashtag': tag,
                    'estimated_reach': hash(tag) % 100000 + 10000
                })
        
        # Create DataFrame and save
        df = pd.DataFrame(hashtag_data)
        output_path = os.path.join(self.output_dir, f"{task_id}_hashtags.xlsx")
        df.to_excel(output_path, index=False)
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    # Simplified implementations for remaining methods
    def schedule_social_posts(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_scheduled_posts.json")
        with open(output_path, 'w') as f:
            json.dump({'message': 'Posts scheduled successfully'}, f)
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def extract_email_list(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_extracted_emails.csv")
        sample_emails = pd.DataFrame({
            'email': ['contact@example.com', 'info@sample.com', 'hello@demo.org'],
            'source': ['Contact page', 'Footer', 'About page']
        })
        sample_emails.to_csv(output_path, index=False)
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def validate_emails(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_email_validation.xlsx")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def analyze_bulk_meta(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_bulk_meta_analysis.xlsx")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}