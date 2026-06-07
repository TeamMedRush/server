from mrs.core.server import serve
from mrs.routes import load_routes
from mrs.services.seed import seed_medicines

def main():
  load_routes()
  seed_medicines()
  serve()

if __name__ == "__main__":
  main()


