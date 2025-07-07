from src.controller import ModMenuController

def main():
    """Função principal para iniciar a aplicação."""
    try:
        app = ModMenuController()
        app.run()
    except Exception as e:
        # Um log de fallback caso a UI falhe ao iniciar
        print(f"Ocorreu um erro fatal ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    main()