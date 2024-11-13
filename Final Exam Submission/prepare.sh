#!/bin/bash

#Get the directory where the script is located
script_dir="$(dirname "$0")"

#Paths for input and output files, using relative paths
input_file="$script_dir/ms_data_dirty.csv"
output_file="$script_dir/ms_data.csv"
insurance_file="$script_dir/insurance.lst"

#Run generate_dirty_data.py to create the raw data file
python3 "$script_dir/generate_dirty_data.py"

#Remove comment lines, empty lines, and fix extra commas
grep -v '^#' "$input_file" | sed '/^$/d' | sed 's/,,*/,/g' > "$script_dir/cleaned_temp.csv"

#Extract essential columns: patient_id, visit_date, age, education_level, walking_speed
awk -F, 'BEGIN {OFS=","} NR==1 || ($6 >= 2.0 && $6 <= 8.0) {print $1, $2, $4, $5, $6}' "$script_dir/cleaned_temp.csv" > "$output_file"

#Create an insurance.lst file with insurance types
echo -e "Value\nHMO\nPPO" > "$insurance_file"

#Generate a summary of the processed data
echo "Total number of visits:" $(tail -n +2 "$output_file" | wc -l)
echo "First 5 records of cleaned data:"
head -n 5 "$output_file"

#Remove temporary files
rm "$script_dir/cleaned_temp.csv"

echo "Data preparation complete."
echo "Processed data saved to $output_file"
echo "Insurance types saved to $insurance_file"
