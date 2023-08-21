import requests
import datetime

def check_ssl_expiry(domain):
    api_url = f"https://api.ssllabs.com/api/v3/analyze?host={domain}"
    response = requests.get(api_url)
    data = response.json()
    
    # Check if 'endpoints' key is present in the response
    if 'endpoints' in data:
        endpoint_data = data['endpoints'][0]
        
        # Check if 'details' key is present in the endpoint data
        if 'details' in endpoint_data:
            cert_data = endpoint_data['details']['cert']
            
            # Check if 'validity' key is present in the cert data
            if 'validity' in cert_data:
                validity_data = cert_data['validity']
                
                # Check if 'notAfter' key is present in the validity data
                if 'notAfter' in validity_data:
                    expiry_date_str = validity_data['notAfter']
                    expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%dT%H:%M:%SZ")
                    days_until_expiry = (expiry_date - datetime.datetime.utcnow()).days
                    
                    return days_until_expiry
    return None

def main():
    domain_list = ["example.com", "google.com", "github.com"]  # Add your domains here
    
    for domain in domain_list:
        days_until_expiry = check_ssl_expiry(domain)
        
        if days_until_expiry is not None:
            print(f"Domain: {domain}")
            print(f"Days until SSL certificate expiry: {days_until_expiry} days\n")

if __name__ == "__main__":
    main()
