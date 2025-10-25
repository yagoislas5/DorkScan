import argparse
import asyncio
import random
import requests
from playwright.async_api import async_playwright

# Check if the target domain is reachable
def is_domain_valid(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Load common dorks from file
with open('dorks.txt', 'r', encoding='utf-8') as f:
    COMMON_DORKS = f.read().splitlines()

def generate_dorks(domain):
    return [dork.format(domain=domain) for dork in COMMON_DORKS]

# CLI arguments
parser = argparse.ArgumentParser(description="Google Dorking Scanner using Brave Search")
parser.add_argument("domain", help="Target domain (example.com)")

parser.add_argument("--save", "-OG", action="store_true", help="Save results to a file")
args = parser.parse_args()

print(f"\n🔍 Generating dorks for: {args.domain}\n")
dorks = generate_dorks(args.domain)

# Load user agents from file
with open('user-agents.txt', 'r', encoding='utf-8') as f:
    USER_AGENTS = f.read().splitlines()

# Main async function
async def main():
    if not is_domain_valid(args.domain):
        print("Target domain is unreachable or invalid\n")
        return

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])

            for dork in dorks:
                user_agent = random.choice(USER_AGENTS)

                context_args = {
                    "user_agent": user_agent,
                    "extra_http_headers": {
                        "Accept-Language": "en-US,en;q=0.9",
                        "DNT": "1",
                        "Referer": "https://search.brave.com/",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Site": "same-origin",
                    }
                }

                context = await browser.new_context(**context_args)
                page = await context.new_page()

                search_url = f"https://search.brave.com/search?q={dork}"
                await page.goto(search_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(random.randint(3000, 6000))

                results = await page.query_selector_all("a[href^='http']")

                if len(results) >= 1:
                    print(f"[+] DORK: {dork}")
                    print(f"Pages found: {len(results)}")
                    if args.save:
                        with open("results.txt", "a", encoding="utf-8") as f:
                            f.write(f"[+],{dork},{len(results)},{user_agent}\n")

                await context.close()

            await browser.close()
            print("\nScan completed. You can review the results.\n")

    except Exception as e:
        print(f"Execution error: {e}")

# Run the script
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExecution interrupted by user\n")
