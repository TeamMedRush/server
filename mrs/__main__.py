from mrs.core.server import serve
from mrs.routes import load_routes

def main():
  load_routes()
  serve()

if __name__ == "__main__":
  main()

