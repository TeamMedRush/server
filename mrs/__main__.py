from mrs.core.server import serve
from mrs.route import load_routes

def main():
  load_routes()
  serve()

if __name__ == "__main__":
  main()

