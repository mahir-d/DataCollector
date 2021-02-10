import subprocess


class statsCollector:

    def get_stats(self):
        tracks = ["Dev", "DS", "Des", "QA"]
        status = ["New", "Draft", "Cancelled", "Active", "Completed"]

        # for stat in status:

        #     for t in tracks:
        #         subprocess.run(
        #             ["python", "init.py", "/Users/mahirdhall/Desktop/WebScrapping", "2001-01-01", "2021-02-02", "-st", stat, "-tr", t])

        subprocess.run(
            ["python", "init.py", "/Users/mahirdhall/Desktop/WebScrapping", "2001-01-01", "2021-02-02", "-st", "Completed", "-tr", "DS"])


def main():
    sc = statsCollector()
    sc.get_stats()


main()
