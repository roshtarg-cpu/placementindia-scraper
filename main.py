from apify import Actor
from bs4 import BeautifulSoup
import requests
import time
import re
from urllib.parse import urlencode, urljoin

async def main():
    async with Actor:
        # Get input from Apify
        actor_input = await Actor.get_input() or {}
        search_keyword = actor_input.get('searchKeyword', '')
        location = actor_input.get('location', 'All India')
        max_jobs = actor_input.get('maxJobs', 100)
        experience_level = actor_input.get('experienceLevel', 'All')
        industry = actor_input.get('industry', 'All')
        job_type = actor_input.get('jobType', 'All')
        
        Actor.log.info(f'Starting PlacementIndia scraper...')
        Actor.log.info(f'Search: "{search_keyword}" in {location}, Max: {max_jobs}')
        
        # Base URL
        base_url = 'https://www.placementindia.com'
        
        # Build search URL
        search_params = {}
        if search_keyword:
            search_params['seeker_search_keyword'] = search_keyword
        if location and location != 'All India':
            search_params['seeker_search_location'] = location
        
        search_url = f'{base_url}/job-search/search.php'
        if search_params:
            search_url += '?' + urlencode(search_params)
        
        Actor.log.info(f'Search URL: {search_url}')
        
        # Headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.placementindia.com/',
            'Connection': 'keep-alive',
        }
        
        jobs_scraped = 0
        page = 1
        
        while jobs_scraped < max_jobs:
            try:
                # Build pagination URL
                if page > 1:
                    search_params['page'] = page
                    current_url = f'{base_url}/job-search/search.php?' + urlencode(search_params)
                else:
                    current_url = search_url
                
                Actor.log.info(f'Fetching page {page}: {current_url}')
                
                # Fetch the page
                response = requests.get(current_url, headers=headers, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings - PlacementIndia uses various selectors
                job_cards = soup.find_all(['div', 'li'], class_=lambda x: x and ('sjc-iteam' in x or 'job' in x.lower()))
                
                if not job_cards:
                    # Try alternative selectors
                    job_cards = soup.find_all(['div', 'article'], attrs={'data-job': True})
                
                if not job_cards:
                    # Try finding links to job details
                    job_links = soup.find_all('a', href=re.compile(r'/job-search/|/jobs/'))
                    if job_links:
                        job_cards = job_links
                
                if not job_cards:
                    Actor.log.warning(f'No jobs found on page {page}')
                    break
                
                Actor.log.info(f'Found {len(job_cards)} job cards on page {page}')
                
                for job_card in job_cards:
                    if jobs_scraped >= max_jobs:
                        break
                    
                    try:
                        job_data = extract_job_data(job_card, base_url)
                        
                        if job_data and job_data.get('jobTitle'):
                            # Push to dataset
                            await Actor.push_data(job_data)
                            jobs_scraped += 1
                            Actor.log.info(f'✓ Scraped job {jobs_scraped}/{max_jobs}: {job_data.get("jobTitle")}')
                        
                    except Exception as e:
                        Actor.log.warning(f'Error parsing job card: {str(e)}')
                        continue
                
                # Check if there are more pages
                next_page = soup.find('a', class_=lambda x: x and 'next' in x.lower() if x else False)
                if not next_page and jobs_scraped < max_jobs:
                    Actor.log.info('No more pages found')
                    break
                
                page += 1
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                Actor.log.error(f'Error on page {page}: {str(e)}')
                break
        
        Actor.log.info(f'✅ Scraping complete! Total jobs: {jobs_scraped}')


def extract_job_data(job_element, base_url):
    """Extract job data from a job card element"""
    job_data = {
        'jobTitle': '',
        'companyName': '',
        'location': '',
        'salary': '',
        'experience': '',
        'skills': [],
        'jobDescription': '',
        'jobUrl': '',
        'postedDate': '',
        'applicants': '',
        'jobType': ''
    }
    
    try:
        # Job Title
        title_elem = (job_element.find(['h2', 'h3', 'h4', 'a'], class_=lambda x: x and 'job-name' in x if x else False) or
                     job_element.find('a', class_=lambda x: x and 'title' in x.lower() if x else False) or
                     job_element.find(['h2', 'h3', 'h4']))
        
        if title_elem:
            job_data['jobTitle'] = title_elem.get_text(strip=True)
        
        # Job URL
        link_elem = job_element.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            job_data['jobUrl'] = urljoin(base_url, href)
        
        # Company Name
        company_elem = (job_element.find(class_=lambda x: x and 'job-cname' in x if x else False) or
                       job_element.find(class_=lambda x: x and 'company' in x.lower() if x else False))
        if company_elem:
            job_data['companyName'] = company_elem.get_text(strip=True)
        
        # Location
        location_elem = (job_element.find(class_=lambda x: x and 'location' in x.lower() if x else False) or
                        job_element.find('img', alt=lambda x: 'location' in x.lower() if x else False))
        if location_elem:
            if location_elem.name == 'img':
                # Location might be in next sibling
                location_elem = location_elem.find_next_sibling()
            if location_elem:
                job_data['location'] = location_elem.get_text(strip=True)
        
        # Experience
        exp_elem = job_element.find(class_=lambda x: x and 'exp' in x.lower() if x else False)
        if exp_elem:
            job_data['experience'] = exp_elem.get_text(strip=True)
        
        # Salary
        salary_elem = job_element.find(class_=lambda x: x and 'salary' in x.lower() if x else False)
        if salary_elem:
            job_data['salary'] = salary_elem.get_text(strip=True)
        
        # Skills
        skills_elem = job_element.find(class_=lambda x: x and ('skill' in x.lower() or 'sk_list' in x) if x else False)
        if skills_elem:
            skills_text = skills_elem.get_text(strip=True)
            # Split by common delimiters
            skills = re.split(r'[,•|]', skills_text)
            job_data['skills'] = [s.strip() for s in skills if s.strip()][:10]
        
        # Posted Date
        date_elem = job_element.find(class_=lambda x: x and ('date' in x.lower() or 'posted' in x.lower()) if x else False)
        if date_elem:
            job_data['postedDate'] = date_elem.get_text(strip=True)
        
        # Job Type
        type_elem = job_element.find(class_=lambda x: x and 'type' in x.lower() if x else False)
        if type_elem:
            job_data['jobType'] = type_elem.get_text(strip=True)
        
        # Job Description (snippet)
        desc_elem = job_element.find(class_=lambda x: x and 'desc' in x.lower() if x else False)
        if desc_elem:
            job_data['jobDescription'] = desc_elem.get_text(strip=True)[:500]
        
    except Exception as e:
        Actor.log.warning(f'Error extracting job data: {str(e)}')
    
    return job_data


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
