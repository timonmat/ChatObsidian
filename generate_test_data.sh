#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <number_of_files> [starting_number]"
    exit 1
fi

num_files=$1
starting_number=${2:-1}  # Use the second argument if provided, otherwise default to 1
word_file="/usr/share/dict/words"
output_dir="./data/${num_files}"

# Read the word file into an array
IFS=$'\n' read -d '' -ra words < "$word_file"
word_count=${#words[@]}

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

for i in $(seq $starting_number $((starting_number + num_files - 1))); do
    output_file="${output_dir}/file_${i}.md"
    for j in {1..25}; do
        random_line=$(((RANDOM * RANDOM) % word_count))
        random_word="${words[$random_line]}"
        echo -n "${random_word} " >> "$output_file"
    done
    echo "" >> "$output_file"
done
