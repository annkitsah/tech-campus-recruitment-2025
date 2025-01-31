## Solutions Considered

### Approach 1: Linear Search for Logs
Initially, I considered using a linear search to find log entries by looping through all the log lines. This would have been easy to implement but inefficient for large log files, especially for 600MB logs.

### Approach 2: Regular Expressions
I considered using regular expressions to search for logs based on patterns. While this approach can be powerful, it may not be optimal for simple date-based filtering and could slow down for large files.

### Approach 3: Optimized Filtering with Date Prefix
The final approach I selected was filtering log entries based on a date prefix. This method is simple, efficient, and easily scalable for large files.

## Final Solution Summary

I chose the "Optimized Filtering with Date Prefix" approach because it's straightforward, efficient, and scales well with larger log files. By checking for the date prefix directly, we avoid unnecessary complexity and ensure that the solution remains performant even for larger log files (like 600MB logs).

## Steps to Run

1. Clone the repository:
   bash
   git clone https://github.com/yourusername/repository_name.git
   

2. Install dependencies:
   If there are any dependencies, make sure to include them in a requirements.txt file.
   To install dependencies, run:
   bash
   pip install -r requirements.txt
   

3. Run the solution script:
   bash
   python extract_logs.py 2024-12-01
   

4. The output will be saved in the output/ directory.
