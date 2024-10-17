# Script to parse the information from a TextGrid file into a csv file
import os
import csv

# Function to extract intervals from the TextGrid file line-by-line
def extract_intervals_from_textgrid(file_path):
    intervals = []
    current_tier = None
    
    # Open the file given in the filepath, and go line-by-line to identify what information is contained within the line
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Identify the current tier (words or phones (phonemes))
            if 'name =' in line:
                if 'words' in line:
                    current_tier = 'words'
                elif 'phones' in line:
                    current_tier = 'phones'

            # Extract xmin, xmax, and text for each interval
            if line.startswith('intervals ['):
                xmin_line = next(f).strip()
                xmax_line = next(f).strip()
                text_line = next(f).strip()

                xmin = xmin_line.split('=')[1].strip()
                xmax = xmax_line.split('=')[1].strip()
                text = text_line.split('=')[1].strip().strip('"')  # Remove quotes

                intervals.append([current_tier, xmin, xmax, text])

    return intervals

# Function to write intervals to a CSV file
def write_intervals_to_csv(intervals, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['tier', 'xmin', 'xmax', 'text'])  # Write header
        writer.writerows(intervals)

# Main function to process all TextGrid files in a folder
def main(input_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.TextGrid'):
            input_file = os.path.join(input_folder, filename)
            intervals = extract_intervals_from_textgrid(input_file)

            # Create output file name (will be the TextGrid file name with "_extracted" appended to the end)
            output_file = os.path.join(input_folder, f"{os.path.splitext(filename)[0]}_extracted.csv")
            write_intervals_to_csv(intervals, output_file)
            print(f'Data extracted to {output_file}')

if __name__ == '__main__':
    input_folder = '/Users/a/mfa_data/my_corpus_aligned'  # Replace this line with your folder path
    main(input_folder)
