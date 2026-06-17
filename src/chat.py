from search import search_prompt

def main():
    """
    Interface CLI para interação com o sistema de busca semântica.
    
    Fluxo:
    1. Exibe mensagem de boas-vindas
    2. Loop infinito que:
       - Recebe pergunta do usuário
       - Chama search_prompt()
       - Exibe a resposta
       - Permite sair digitando 'sair' ou 'exit'
    """
    
    # MENSAGEM DE BOAS-VINDAS
    print("=" * 60)
    print("🤖 SISTEMA DE BUSCA SEMÂNTICA - RAG com LangChain")
    print("=" * 60)
    print("\n📚 Sistema pronto para responder perguntas sobre o PDF!")
    print("💡 Dica: Digite 'sair' ou 'exit' para encerrar.\n")
    print("=" * 60)
    
    # LOOP PRINCIPAL DO CHAT
    while True:
        try:
            # Receber pergunta do usuário
            print("\n" + "─" * 60)
            pergunta = input("Faça sua pergunta: ").strip()
            print("─" * 60)
            
            # Verificar se o usuário quer sair
            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\n👋 Encerrando o sistema. Até logo!")
                break
            
            # Verificar se a pergunta está vazia
            if not pergunta:
                print("⚠️  Por favor, digite uma pergunta válida.")
                continue
            
            # Processar a pergunta
            print("\n🔍 Buscando informações relevantes...")
            resposta = search_prompt(pergunta)
            
            # Exibir a resposta
            print("\n" + "=" * 60)
            print("RESPOSTA:")
            print("=" * 60)
            print(resposta)
            print("=" * 60)
            
        except KeyboardInterrupt:
            # Capturar Ctrl+C para sair graciosamente
            print("\n\n👋 Encerrando o sistema. Até logo!")
            break
            
        except Exception as e:
            # Capturar erros inesperados
            print(f"\n❌ Erro inesperado: {e}")
            print("Por favor, tente novamente.")

if __name__ == "__main__":
    main()