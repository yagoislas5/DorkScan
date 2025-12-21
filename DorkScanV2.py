#!/usr/bin/env python3
import argparse
import os
import subprocess
import json
from urllib.parse import urlparse

# =============================
# ===== COLORES TERMINAL =====
# =============================
RED = "\033[31m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# =============================
# ===== ASCII BANNER ==========
# =============================
BANNER = f"""
{CYAN}██████╗  ██████╗ ██████╗ ██╗  ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██╔════╝██╔══██╗████╗  ██║
██║  ██║██║   ██║██████╔╝█████╔╝ ███████╗██║     ███████║██╔██╗ ██║
██║  ██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██║     ██╔══██║██║╚██╗██║
██████╔╝╚██████╔╝██║  ██║██║  ██╗███████║╚██████╗██║  ██║██║ ╚████║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
        {YELLOW}DorkScan – Subdomain Finder & HTTP Classifier{RESET}
"""

# =============================
# ===== EJECUTAR COMANDO ======
# =============================
def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True)
        return out.decode().strip().split("\n")
    except:
        return []

# =============================
# ===== SUBDOMAIN ENUM ========
# =============================
def gather_subdomains(domain, outdir):
    all_subs = set()

    tools = {
        "subfinder": f"subfinder -silent -d {domain}",
        "assetfinder": f"assetfinder --subs-only {domain}",
        "amass": f"amass enum -d {domain}",
        "findomain": f"findomain -t {domain} -q",
        "sublist3r": f"sublist3r -d {domain} -o {outdir}/sublist3r.txt >/dev/null 2>&1"
    }

    print(f"{CYAN}=== Procesando {domain} ==={RESET}")

    # subfinder
    print(f"{YELLOW}[+] Ejecutando subfinder...{RESET}")
    subs = run_cmd(tools["subfinder"])
    print(f"{GREEN}[+] subfinder: {len(subs)} subdominios{RESET}")
    all_subs.update(subs)

    # assetfinder
    print(f"{YELLOW}[+] Ejecutando assetfinder...{RESET}")
    subs = run_cmd(tools["assetfinder"])
    print(f"{GREEN}[+] assetfinder: {len(subs)} subdominios{RESET}")
    all_subs.update(subs)

    # amass
    print(f"{YELLOW}[+] Ejecutando amass...{RESET}")
    subs = run_cmd(tools["amass"])
    print(f"{GREEN}[+] amass: {len(subs)} subdominios{RESET}")
    all_subs.update(subs)

    # findomain
    print(f"{YELLOW}[+] Ejecutando findomain...{RESET}")
    subs = run_cmd(tools["findomain"])
    print(f"{GREEN}[+] findomain: {len(subs)} subdominios{RESET}")
    all_subs.update(subs)

    # sublist3r
    print(f"{YELLOW}[+] Ejecutando sublist3r...{RESET}")
    os.system(tools["sublist3r"])
    try:
        with open(f"{outdir}/sublist3r.txt") as f:
            subs = [x.strip() for x in f.readlines()]
        print(f"{GREEN}[+] sublist3r: {len(subs)} subdominios{RESET}")
        all_subs.update(subs)
    except:
        pass

    # guardar archivo
    final_file = f"{outdir}/{domain}_subdomains.txt"
    with open(final_file, "w") as f:
        for s in sorted(all_subs):
            f.write(s + "\n")

    print(f"{GREEN}[+] Subdominios totales: {len(all_subs)} guardados en {final_file}{RESET}")
    return final_file

# =============================
# ===== HTTPX CLASSIFIER ======
# =============================
def classify_with_httpx(sub_file, outdir):
    print(f"{YELLOW}[+] Ejecutando httpx sobre {sub_file}{RESET}")

    cmd = f"httpx -l {sub_file} -json -silent"
    raw = run_cmd(cmd)

    results = {}
    timeouts = set()

    for line in raw:
        try:
            j = json.loads(line)
        except:
            continue

        url = j.get("url") or j.get("input") or j.get("host")
        status = j.get("status_code")

        parsed = urlparse(url) if url else None
        host = parsed.netloc.split(":")[0] if parsed and parsed.netloc else (parsed.path if parsed else None)

        if not host:
            continue

        if status:
            status = str(status)
            if status not in results:
                results[status] = set()
            results[status].add(host)
        else:
            # si no hay status_code, lo consideramos timeout/error
            timeouts.add(host)

    # guardar archivos por código
    for code, hosts in results.items():
        outfile = f"{outdir}/{code}.txt"
        with open(outfile, "w") as f:
            for h in sorted(hosts):
                f.write(h + "\n")
        print(f"{GREEN}[✓] {len(hosts)} subdominios guardados en {outfile}{RESET}")

    # guardar timeouts si existen
    if timeouts:
        outfile = f"{outdir}/timeout.txt"
        with open(outfile, "w") as f:
            for h in sorted(timeouts):
                f.write(h + "\n")
        print(f"{RED}[!] {len(timeouts)} subdominios sin respuesta guardados en {outfile}{RESET}")

    print(f"{GREEN}[✓] Clasificación finalizada.{RESET}")

# =============================
# ============ MAIN ===========
# =============================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", required=True, help="Dominio objetivo")
    args = parser.parse_args()

    domain = args.d
    outdir = f"output/{domain}"
    os.makedirs(outdir, exist_ok=True)

    print(BANNER)

    sub_file = gather_subdomains(domain, outdir)
    classify_with_httpx(sub_file, outdir)

if __name__ == "__main__":
    main()
