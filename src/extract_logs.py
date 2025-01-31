import sys
from datetime import datetime
import mmap
from pathlib import Path

class LogExtractor:
    def _init_(self, log_file_path):
        self.log_file_path = log_file_path
        self.date_format = "%Y-%m-%d"
        self.timestamp_length = 10  

    def binary_search_position(self, target_date, mm, start, end):
        """Perform binary search to find the position of target date in file."""
        while start <= end:
            mid = (start + end) // 2
            
            # Seek to nearest newline before mid
            while mid > 0 and mm[mid-1:mid] != b'\n':
                mid -= 1
            
            # Read the date from current position
            try:
                current_date = mm[mid:mid+self.timestamp_length].decode()
                current_date = datetime.strptime(current_date, self.date_format)
                target = datetime.strptime(target_date, self.date_format)
                
                if current_date == target:
                    # Found a matching date, now find the first occurrence
                    while mid > 0:
                        prev_pos = mid - 1
                        while prev_pos > 0 and mm[prev_pos-1:prev_pos] != b'\n':
                            prev_pos -= 1
                        prev_date = mm[prev_pos:prev_pos+self.timestamp_length].decode()
                        try:
                            if datetime.strptime(prev_date, self.date_format) != target:
                                break
                            mid = prev_pos
                        except ValueError:
                            break
                    return mid
                elif current_date < target:
                    start = mid + 1
                else:
                    end = mid - 1
            except ValueError:
                # If we can't parse the date, try the next position
                start = mid + 1
                
        return -1

    def extract_logs(self, target_date):
        """Extract logs for the specified date and save to output file."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"output_{target_date}.txt"

        try:
            with open(self.log_file_path, 'rb') as f:
                # Memory map the file for efficient reading
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                
                # Find the starting position of the target date
                start_pos = self.binary_search_position(target_date, mm, 0, len(mm))
                
                if start_pos == -1:
                    print(f"No logs found for date: {target_date}")
                    return

                # Read and write matching logs
                with open(output_file, 'w') as out_f:
                    current_pos = start_pos
                    while current_pos < len(mm):
                        # Find next newline
                        newline_pos = mm.find(b'\n', current_pos)
                        if newline_pos == -1:
                            newline_pos = len(mm)
                        
                        # Read the line
                        line = mm[current_pos:newline_pos].decode()
                        
                        # Check if this line starts with our target date
                        if not line.startswith(target_date):
                            break
                        
                        out_f.write(line + '\n')
                        current_pos = newline_pos + 1

                mm.close()
                print(f"Logs extracted to: {output_file}")

        except FileNotFoundError:
            print(f"Error: Log file not found at {self.log_file_path}")
        except Exception as e:
            print(f"Error processing logs: {str(e)}")

def main():

    target_date = sys.argv[1]
    log_file_path = "test_logs.log"
    
    extractor = LogExtractor(log_file_path)
    extractor.extract_logs(target_date)

if _name_ == "_main_":
    main()
