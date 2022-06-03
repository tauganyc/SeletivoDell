import csv
#abre o csv e lê linha a linha
csvfile = "TA_PRECO_MEDICAMENTO.csv"
file=open(csvfile,'r',encoding='utf-8')
reader=csv.DictReader(file,delimiter=';')
#cria um array para salvar os dados dos medicamentos pelo nome
dicionarioNome=dict()
dicionarioCodigo=dict()
negativa=0
positiva=0
neutra=0
#indexa o arquivo para ler as variaveis
for row in reader:
    #salva os dados da questao 3
    if row["LISTA DE CONCESSÃO DE CRÉDITO TRIBUTÁRIO (PIS/COFINS)"]=='Negativa':
        negativa+=1
    elif row["LISTA DE CONCESSÃO DE CRÉDITO TRIBUTÁRIO (PIS/COFINS)"]=='Positiva':
        positiva+=1
    elif row["LISTA DE CONCESSÃO DE CRÉDITO TRIBUTÁRIO (PIS/COFINS)"]=='Neutra':
        neutra+=1
    #salva os dados da questao 2
    codigo=row["EAN 1"]
    pmc=row["PMC 0%"].strip().replace(',', '.')
    if pmc != "":
        pmc = float(pmc)
        if codigo in dicionarioCodigo:
            dicionarioCodigo[codigo].append((pmc))
        else:
            dicionarioCodigo[codigo]=[(pmc)]
    
    #salva os dados da questão 1, como não tinha no csv a variavel nome utilizei a substância para continuar a execução
    if row["COMERCIALIZAÇÃO 2020"]=='Sim':
        nome=row["SUBSTÂNCIA"]
        produto=row["PRODUTO"]
        apresentacao=row["APRESENTAÇÃO"]
        valor=row["PF Sem Impostos"]
        if nome in dicionarioNome:
            dicionarioNome[nome].append((produto,apresentacao,valor))
        else:
            dicionarioNome[nome]=[(produto,apresentacao,valor)]
file.close()
controle=-1
while controle!=0:
    controle: str =input("digite 1 para pesquisar pelo nome\ndigite 2 para pesquisar pelo codigo de barras\ndigite 3 para a lista de concessao de credito tributario (pis/cofins)\ndigite 0 para sair e finalizar o programa\nqual sua opção? ")
    #verifica se o controle é inteiro, se não for muda para o controle para um valor que irá voltar para o inico do laço
    try:
        controle: int = int(controle)
    except Exception:
        controle = -1
        
    #pesquisa pelo nome
    if controle==1:
        verifica=0
        while True:
            pesquisa=input("Digite o medicamento ou SAIR para voltar ao menu: ")
            print()
            
            if pesquisa.upper() == "SAIR":
                break
            
            resultados=list()
            # FAZ PESQUISA
            for chave in dicionarioNome:
                #.startswith() compara oque foi digitado com oque tem no array
                #.upper() coloca a variavel em CAPS para pesquisar o dado que está em caps no csv
                if chave.startswith(pesquisa.upper()):
                    resultados.append((chave, dicionarioNome[chave]))
                    verifica=1
            
            # MOSTRA o resultado
            print(f"pesquisando {pesquisa}\n")
            if verifica==1:
                for chave, resultado in resultados:   
                    print(f"Substancia: {chave}")
                    for prod, apr, valor in resultado:
                        print(f"Produto: {prod} | Apresentacao: {apr} | Valor: {valor}")
            else:
                print("Error: Tente novamente")
    #pesquisa por codigo de barras
    elif controle==2:
        while True:
            pesquisa=input("Digite o codigo de barras ou SAIR para voltar ou menu: ")
            print()
            #irá sempre colocar o resultado em caps para comparar e assim ver se sai ou fica no laço
            if pesquisa.upper() ==  "SAIR":
                break
            
            print(f"pesquisando codigo {pesquisa}")
            resultado=""
            #se o resultado não for encontrado ele volta pro inicio do laço
            try:
                resultado = dicionarioCodigo[pesquisa]               
            except KeyError:
                print("Código não encontrado\n")
                continue
            
            maior=float(0)
            menor=resultado[0]
            for pmc in resultado:
                if pmc < menor:
                    menor = pmc
                elif pmc > maior:
                    maior = pmc
            print(f"O maior PMC 0% é {maior}")
            print(f"O menor PMC 0% é {menor}")
            print(f"A diferença entre eles é {maior-menor:.2f}")
    #mostra o gráfico
    elif controle==3:
        total=positiva+negativa+neutra
        porcentagemPositiva=float((positiva*100.0)/total)
        porcentagemNeutra=float((neutra*100.0)/total)
        porcentagemNegativa=float((negativa*100.0)/total)
        print("\nClassificação   Percentual   Gráfico")
        print(f"Negativa         {porcentagemNegativa:.2f}%      ",end='')
        print("*"*int(porcentagemNegativa))
        print(f"Neutra           {porcentagemNeutra:.2f}%      ",end='')
        print("*"*int(porcentagemNeutra))
        print(f"Positiva         {porcentagemPositiva:.2f}%      ",end='')
        print("*"*int(porcentagemPositiva))
        print(f"Total            100%")
        input("Aperte ENTER para voltar ao menu\n")
    elif controle!=0:
        print("\nError, digite um valor valido\n")
    