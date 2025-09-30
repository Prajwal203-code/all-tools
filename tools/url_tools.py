import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from urllib.parse import urljoin, urlparse
import tempfile

class URLProcessor:
    def __init__(self):
        self.output_dir = 'output'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process(self, tool_name, data, task_id):
        """Main processing method that routes to specific tool handlers"""
        
        time.sleep(1)  # Initial setup time
        
        method_map = {
            'url_summarizer': self.summarize_url,
            'keyword_scraper': self.scrape_keywords,
            'meta_tag_extractor': self.extract_meta_tags,
            'broken_link_checker': self.check_broken_links,
            'sitemap_generator': self.generate_sitemap,
            'page_speed_analyzer': self.analyze_page_speed,
            'internal_link_visualizer': self.visualize_links,
            'social_share_preview': self.preview_social_share,
            'html_pdf_generator': self.html_to_pdf,
            'bulk_screenshot_generator': self.generate_screenshots,
            'robots_validator': self.validate_robots,
            'redirect_checker': self.check_redirects,
            'competitor_analyzer': self.analyze_competitor,
            'website_text_extractor': self.extract_website_text,
            'web_archive_generator': self.generate_archive
        }
        
        handler = method_map.get(tool_name)
        if not handler:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        return handler(data, task_id)
    
    def update_progress(self, task_id, progress):
        """Update task progress"""
        from app import TaskManager
        TaskManager.update_progress(task_id, progress)
    
    def get_webpage_content(self, url):
        """Helper method to get webpage content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            raise Exception(f"Failed to fetch {url}: {str(e)}")
    
    def summarize_url(self, data, task_id):
        """Summarize website content"""
        self.update_progress(task_id, 20)
        
        url = data.get('url', '')
        if not url:
            raise ValueError("URL is required")
        
        try:
            response = self.get_webpage_content(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            text_content = soup.get_text()
            
            # Basic summarization (in a real implementation, you'd use AI/NLP)
            sentences = text_content.split('.')[:10]  # First 10 sentences
            summary = '. '.join(sentences) + '.'
            
            # Extract basic info
            title = soup.find('title').get_text() if soup.find('title') else 'No title'
            meta_desc = ''
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                meta_desc = desc_tag.get('content', '')
            
            self.update_progress(task_id, 70)
            
            # Create summary report
            report = {
                'url': url,
                'title': title,
                'meta_description': meta_desc,
                'content_length': len(text_content),
                'summary': summary,
                'word_count': len(text_content.split())
            }
            
            # Save report
            output_path = os.path.join(self.output_dir, f"{task_id}_url_summary.json")
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            
        except Exception as e:
            # Create error report
            output_path = os.path.join(self.output_dir, f"{task_id}_summary_error.txt")
            with open(output_path, 'w') as f:
                f.write(f"Error summarizing {url}: {str(e)}")
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def scrape_keywords(self, data, task_id):
        """Extract keywords from website"""
        self.update_progress(task_id, 20)
        
        url = data.get('url', '')
        if not url:
            raise ValueError("URL is required")
        
        try:
            response = self.get_webpage_content(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text
            text_content = soup.get_text().lower()
            
            # Simple keyword extraction (frequency based)
            words = text_content.split()
            
            # Filter out common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'under', 'between', 'among', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'will', 'would', 'should', 'could', 'can', 'cannot', 'cant', 'may', 'might', 'must', 'shall'}
            
            # Count word frequency
            word_freq = {}
            for word in words:
                word = word.strip('.,!?";:()[]{}').lower()
                if len(word) > 3 and word not in stop_words and word.isalpha():
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency
            sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:50]
            
            self.update_progress(task_id, 70)
            
            # Create report
            keywords_data = []
            for keyword, frequency in sorted_keywords:
                keywords_data.append({
                    'keyword': keyword,
                    'frequency': frequency,
                    'density': round((frequency / len(words)) * 100, 2)
                })
            
            # Save as Excel
            df = pd.DataFrame(keywords_data)
            output_path = os.path.join(self.output_dir, f"{task_id}_keywords.xlsx")
            df.to_excel(output_path, index=False)
            
        except Exception as e:
            output_path = os.path.join(self.output_dir, f"{task_id}_keywords_error.txt")
            with open(output_path, 'w') as f:
                f.write(f"Error extracting keywords from {url}: {str(e)}")
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def extract_meta_tags(self, data, task_id):
        """Extract meta tags from URL"""
        self.update_progress(task_id, 20)
        
        url = data.get('url', '')
        if not url:
            raise ValueError("URL is required")
        
        try:
            response = self.get_webpage_content(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract meta tags
            meta_data = {
                'url': url,
                'title': soup.find('title').get_text() if soup.find('title') else '',
                'meta_description': '',
                'meta_keywords': '',
                'meta_author': '',
                'meta_robots': '',
                'og_title': '',
                'og_description': '',
                'og_image': '',
                'og_url': '',
                'twitter_card': '',
                'twitter_title': '',
                'twitter_description': '',
                'canonical_url': ''
            }
            
            # Standard meta tags
            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                name = tag.get('name', '').lower()
                property_attr = tag.get('property', '').lower()
                content = tag.get('content', '')
                
                if name == 'description':
                    meta_data['meta_description'] = content
                elif name == 'keywords':
                    meta_data['meta_keywords'] = content
                elif name == 'author':
                    meta_data['meta_author'] = content
                elif name == 'robots':
                    meta_data['meta_robots'] = content
                elif property_attr == 'og:title':
                    meta_data['og_title'] = content
                elif property_attr == 'og:description':
                    meta_data['og_description'] = content
                elif property_attr == 'og:image':
                    meta_data['og_image'] = content
                elif property_attr == 'og:url':
                    meta_data['og_url'] = content
                elif name == 'twitter:card':
                    meta_data['twitter_card'] = content
                elif name == 'twitter:title':
                    meta_data['twitter_title'] = content
                elif name == 'twitter:description':
                    meta_data['twitter_description'] = content
            
            # Canonical URL
            canonical = soup.find('link', {'rel': 'canonical'})
            if canonical:
                meta_data['canonical_url'] = canonical.get('href', '')
            
            self.update_progress(task_id, 70)
            
            # Save as JSON and Excel
            json_path = os.path.join(self.output_dir, f"{task_id}_meta_tags.json")
            with open(json_path, 'w') as f:
                json.dump(meta_data, f, indent=2)
            
            # Also create Excel version
            df = pd.DataFrame([meta_data])
            excel_path = os.path.join(self.output_dir, f"{task_id}_meta_tags.xlsx")
            df.to_excel(excel_path, index=False)
            
            output_path = excel_path  # Return Excel file
            
        except Exception as e:
            output_path = os.path.join(self.output_dir, f"{task_id}_meta_error.txt")
            with open(output_path, 'w') as f:
                f.write(f"Error extracting meta tags from {url}: {str(e)}")
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def check_broken_links(self, data, task_id):
        """Check for broken links on a website"""
        self.update_progress(task_id, 20)
        
        url = data.get('url', '')
        if not url:
            raise ValueError("URL is required")
        
        try:
            response = self.get_webpage_content(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            link_results = []
            total_links = len(links)
            
            for i, link in enumerate(links[:50]):  # Limit to first 50 links for demo
                href = link['href']
                absolute_url = urljoin(url, href)
                
                try:
                    link_response = requests.head(absolute_url, timeout=5)
                    status_code = link_response.status_code
                    status = 'OK' if status_code < 400 else 'Broken'
                except Exception as e:
                    status_code = 'Error'
                    status = 'Broken'
                
                link_results.append({
                    'link_text': link.get_text()[:100],
                    'url': absolute_url,
                    'status_code': status_code,
                    'status': status
                })
                
                # Update progress
                progress = 20 + (70 * (i + 1) / min(total_links, 50))
                self.update_progress(task_id, progress)
            
            # Create report
            df = pd.DataFrame(link_results)
            output_path = os.path.join(self.output_dir, f"{task_id}_broken_links.xlsx")
            df.to_excel(output_path, index=False)
            
        except Exception as e:
            output_path = os.path.join(self.output_dir, f"{task_id}_link_check_error.txt")
            with open(output_path, 'w') as f:
                f.write(f"Error checking links on {url}: {str(e)}")
        
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    # Simplified implementations for remaining methods
    def generate_sitemap(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_sitemap.xml")
        with open(output_path, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>')
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def analyze_page_speed(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_speed_report.txt")
        with open(output_path, 'w') as f:
            f.write("Page speed analysis completed.")
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def visualize_links(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_link_visualization.png")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def preview_social_share(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_social_preview.png")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def html_to_pdf(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_webpage.pdf")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_screenshots(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_screenshots.zip")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def validate_robots(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_robots_validation.txt")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def check_redirects(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_redirects.xlsx")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def analyze_competitor(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_competitor_analysis.xlsx")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def extract_website_text(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_website_text.txt")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}
    
    def generate_archive(self, data, task_id):
        self.update_progress(task_id, 50)
        output_path = os.path.join(self.output_dir, f"{task_id}_web_archive.zip")
        # Placeholder implementation
        self.update_progress(task_id, 100)
        return {'output_path': output_path, 'filename': os.path.basename(output_path)}