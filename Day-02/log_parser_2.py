from collections import Counter

log_counts = Counter()
errors = []

with open("log.txt") as f:
    for line in f:
        parts = line.strip().split(" ",1)
        level = parts[0]
        if level in ["INFO", "ERROR", "WARNING"]:
            log_counts[level]+=1
        if level == "ERROR":
            errors.append(parts[1] if len(parts) > 1 else "")

for level, count in log_counts.items():
    print(f"{level}: {count}")
print("\nError logs:")
for err in errors:
    print(f" - {err}")
        
