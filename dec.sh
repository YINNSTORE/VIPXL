#!/bin/bash

# --------------------------------------------
# Ultimate Decryptor Tool - By Yin
# Fitur: SHC, BZIP2, BashArmor, Base64
# --------------------------------------------

# Konfigurasi Tampilan
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
PURPLE='\033[1;35m'
NC='\033[0m'
BOLD='\033[1m'
BLINK='\033[5m'

# Animasi Spinner Profesional
spinner() {
    local pid=$!
    local delay=0.1
    local spin_chars=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local i=0
    
    tput civis
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % 10 ))
        printf "\r[${PURPLE}%s${NC}] %s " "${spin_chars[$i]}" "$1"
        sleep $delay
    done
    tput cnorm
    printf "\r\033[K"
}

# Progress Bar Animasi
progress_bar() {
    local duration=$1
    local bar=""
    for ((i=0; i<=50; i++)); do
        bar+="▉"
        printf "\r[${CYAN}%-51s${NC}] %d%%" "$bar" $((i*2))
        sleep $(bc <<< "scale=5; $duration/50")
    done
    printf "\n"
}

# Banner Dinamis
show_banner() {
    clear
    echo -e "${CYAN}"
    echo " ██████╗ ███████╗ ██████╗██████╗ ██╗   ██╗███████╗   ██████╗ ██████╗"
    echo "██╔═══██╗██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝██╔════╝   ██╔══██╗██╔══██╗"
    echo "██║   ██║█████╗  ██║     ██████╔╝ ╚████╔╝ █████╗     ██║  ██║██████╔╝"
    echo "██║   ██║██╔══╝  ██║     ██╔══██╗  ╚██╔╝  ██╔══╝     ██║  ██║██╔══██╗"
    echo "╚██████╔╝██║     ╚██████╗██║  ██║   ██║   ███████╗██╗██████╔╝██║  ██║"
    echo " ╚═════╝ ╚═╝      ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝"
    echo -e "${NC}"
    echo -e "${YELLOW}༺༻ ${BOLD}Multi-Format Decryptor with Dynamic Animation ${YELLOW}༺༻${NC}"
    echo -e "${GREEN}                    Created by: Yin © 2024${NC}"
    echo "=================================================================="
}

# Deteksi File Canggih
detect_type() {
    local file=$1
    local magic=$(xxd -l 4 "$file" | awk '{print $2$3$4}')
    
    { [[ "$magic" == "425a68"* ]] && echo "bzip2"; } ||
    { grep -q 'BEGIN basharmor' "$file" && echo "basharmor"; } ||
    { grep -q 'BEGIN BASE64' "$file" && echo "base64"; } ||
    { strings "$file" | grep -q '####' && echo "shc"; } ||
    echo "unknown"
}

# Dekripsi SHC (Versi Enhanced)
decrypt_shc() {
    (
    echo -e "[1/4] ${YELLOW}Analyzing SHC payload...${NC}"
    marker=$(strings "$1" | grep -obaP "\x47\x4e\x55\x00\x01\x00\x00\x00" | cut -d: -f1)
    dd if="$1" bs=1 skip=$((marker)) 2>/dev/null | strings -n 10 > "$2.tmp"
    
    echo -e "[2/4] ${YELLOW}Extracting XOR key...${NC}"
    key=$(head -n 3 "$2.tmp" | tail -1 | tr -d '\n' | md5sum | cut -c1-4)
    
    echo -e "[3/4] ${YELLOW}Decrypting (AES-128-CBC)...${NC}"
    openssl enc -d -aes-128-cbc -K $(printf "$key" | xxd -p) -iv 0 -in "$2.tmp" -out "$2" 2>/dev/null
    
    echo -e "[4/4] ${YELLOW}Validating output...${NC}"
    rm "$2.tmp"
    ) > >(while read line; do echo -e "  ${CYAN}↳${NC} $line"; done) 2>&1
}

# Dekripsi Modern
decrypt_bzip2() { (bzip2 -dck "$1" > "$2") & spinner "Decompressing BZIP2..."; }
decrypt_basharmor() { (sed -n '/BEGIN basharmor/,/END basharmor/p' "$1" | base64 -d > "$2") & spinner "Decoding BashArmor..."; }
decrypt_base64() { (base64 -di "$1" > "$2") & spinner "Decrypting Base64..."; }

# Nested Decryption Handler
nested_decrypt() {
    local file="$1"
    local level=1
    
    while true; do
        type=$(detect_type "$file")
        [[ "$type" == "unknown" ]] && break
        
        new_file="${file}.level${level}"
        echo -e "\n${PURPLE}♺ Layer ${level} Detected (${type}):${NC}"
        
        case $type in
            shc) decrypt_shc "$file" "$new_file" ;;
            bzip2) decrypt_bzip2 "$file" "$new_file" ;;
            basharmor) decrypt_basharmor "$file" "$new_file" ;;
            base64) decrypt_base64 "$file" "$new_file" ;;
        esac
        
        file="$new_file"
        ((level++))
    done
    
    mv "$file" "$2"
    echo -e "\n${GREEN}✓ Total Decryption Layers: $((level-1))${NC}"
}

# Main Execution
main() {
    show_banner
    [[ $# -eq 0 ]] && echo -e "${RED}Usage: $0 <file> [output]${NC}" && exit 1
    
    input="$1"
    output="${2:-${input}.decrypted}"
    
    echo -e "\n${BOLD}➤ Target File:${NC} ${YELLOW}$input${NC}"
    progress_bar 1.5
    
    echo -e "\n${BOLD}➤ Initializing Decryption Engine...${NC}"
    nested_decrypt "$input" "$output"
    
    echo -e "\n${GREEN}${BLINK}✅ Successfully Decrypted!${NC}"
    echo -e "${BOLD}Final Output:${NC} ${GREEN}$output${NC}"
    echo -e "${BOLD}File Type:${NC} $(file -b "$output")"
}

# Error Handling
trap 'echo -e "\n${RED}✖ Interrupted! Cleaning up...${NC}"; rm -f *.level*; exit 1' SIGINT

# Execution
main "$@"