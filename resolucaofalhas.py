'''BIBLIOTECA UTILIZADAS'''
import json
import os
import pandas as pd
import patoolib
import re
import shutil

class Automacao():
    # Variáveis usadas em diversas funções
    def __init__(self):
        self.path = 'C:/Users/G053/Desktop/FALHAS'
        self.stack = {}
        self.twm = {}
        self.parser = {}
        self.regex = {}
        Automacao.sheets(self)

    # Listar arquivos de uma pasta
    def diretorio(self, pasta):
        arquivos = []
        for dir, subpastas, arq in os.walk(f'{self.path}/{pasta}'):
            for arquivo in arq:
                arquivos.append(arquivo)
        return arquivos

    def sheets(self):
        csvDataframe = pd.read_csv('C:/Users/G053/Downloads/Pesquisa Fatura NotOk.csv')
        # Dados principais
        transction = (csvDataframe['fields.elasticInvoiceMessage.TransactionId']).to_list()
        fornecedor = (csvDataframe['fields.elasticInvoiceMessage.Supplier']).to_list()
        cliente = (csvDataframe['fields.elasticInvoiceMessage.Customer']).to_list()
        description = (csvDataframe['fields.elasticInvoiceMessage.Description']).to_list()

        for i, value in enumerate(transction):
            self.stack[value] = description[i]
            self.twm[value] = cliente[i]
            self.parser[value] = fornecedor[i]
        Automacao.tratativas(self)
    
    def organizarcliente(self, path):
        # Organizar as falhas em pastas
        gedfiles = Automacao.diretorio(self, path)
        for i in gedfiles:
            try:
                os.makedirs(f"{self.path}/{path}/{self.twm[i.replace('.zip', '')]}", exist_ok=True)
                shutil.move(f"{self.path}/{path}/{i}", f"{self.path}/{path}/{self.twm[i.replace('.zip', '')]}")
            except KeyError:
                pass
            except shutil.Error:
                pass

    # Tratando as falhas  e gerando os relatórios
    def tratativas(self):
        # Id do fornecedor diferente do cadastrado
        unzip = Automacao.diretorio(self, 'ID')
        pathID = f'{self.path}/ID'

        for arquivo in unzip:
            try:
                patoolib.extract_archive(f'{pathID}/{arquivo}', outdir=f"{pathID}/{arquivo.replace('.zip', '')}")
                match = re.findall(r'id.*?(\d+)', self.stack[arquivo.replace('.zip', '')])

                for dir, subpastas, arq in os.walk(f"{pathID}/{arquivo.replace('.zip', '')}"):
                    for fatura in arq:
                        if '.zip' in fatura:
                            patoolib.extract_archive(f"{pathID}/{arquivo.replace('.zip', '')}/{fatura}", outdir=f"{pathID}/{arquivo.replace('.zip', '')}/{fatura.replace('.zip', '')}")
                        # Alterando o ID do fornecedor
                        try:
                            txt = (open(f"{pathID}/{arquivo.replace('.zip', '')}/{fatura.replace('.zip', '')}/invoice.txt", 'r')).readlines()
                            obs = open(f'C:/Users/G053/Desktop/Anotações/ID fornecedor.txt', 'a')
                            arq = json.loads(txt[0])
                            if arq['IdFornecedor'] == int(match[0]):
                                obs.write(f"\n{self.twm[arquivo.replace('.zip', '')]}; {arq['NumeroContaAglutinada']}; {int(match[0])}; {int(match[1])}")
                                obs.close()
                                arq['IdFornecedor'] = int(match[1])
                                texto = json.dumps(arq)
                                txt_novo = open(f"{pathID}/{arquivo.replace('.zip', '')}/{fatura.replace('.zip', '')}/invoice.txt", 'w', encoding='UTF-8')
                                txt_novo.write(texto)
                                txt_novo.close()
                                # Compactando arquivos após alterção
                                shutil.make_archive(f"{pathID}/{arquivo.replace('.zip', '')}/{fatura.replace('.zip', '')}", 'zip', f"{pathID}/{arquivo.replace('.zip', '')}/{fatura.replace('.zip', '')}")
                                shutil.rmtree(f"{pathID}/{arquivo.replace('.zip', '')}/{fatura.replace('.zip', '')}")
                                shutil.make_archive(f"{pathID}/{arquivo.replace('.zip', '')}", 'zip', f"{pathID}/{arquivo.replace('.zip', '')}")
                                shutil.rmtree(f"{pathID}/{arquivo.replace('.zip', '')}")
                        except:
                            pass
            except patoolib.util.PatoolError:
                pass
        # Erros Parser
        paths = ['Razão Social', 'Conta Aglutinada', 'Conta +20', 'Fatura TWM', 'GED', 'Emissão', 'Código de barras', 'Serviços']
        for path in paths:
            falhas = Automacao.diretorio(self, path)
            for i in falhas:
                if not 'batch command' in self.stack[i.replace('.zip', '')]:
                    obs = open(f'C:/Users/G053/Desktop/Anotações/Parser.txt', 'a')
                    obs.write(f"\n{(self.parser[i.replace('.zip', '')]).upper()}; {path}")
                    obs.close()

                if path == 'GED':
                    stack = self.stack[i.replace('.zip', '')]
                    conta = re.findall(r"\'.*\'", stack)
                    ged = re.findall(r"GED.*\-A", stack)
                    obs = open(f'C:/Users/G053/Desktop/Anotações/GED Files.txt', 'a')
                    obs.write(f"\n{(self.twm[i.replace('.zip', '')])}; {conta[0]}; {ged[0]}")
                    obs.close()

        # Annie Transction
        erros = ['NotaFiscal', 'DataReferencia', 'ServicosFaturados', 'Impostos']
        for i in erros:
            unzip = Automacao.diretorio(self, i)
            path = f'{self.path}/{i}'

            for arquivo in unzip:
                try:
                    patoolib.extract_archive(f'{path}/{arquivo}', outdir=f"{path}/{arquivo.replace('.zip', '')}")

                    for dir, subpastas, arq in os.walk(f"{path}/{arquivo.replace('.zip', '')}"):
                        for annie in arq:
                            if annie == 'annie-integration-info.json':
                                # Alterando o canonico da Annie
                                try:
                                    with open(f"{path}/{arquivo.replace('.zip', '')}/{annie}", encoding='utf-8') as meu_json:
                                        dados = json.load(meu_json)
                                        dados[f'{i}'] = ''
                                    with open(f"{path}/{arquivo.replace('.zip', '')}/{annie}", 'w') as meu_json:
                                        texto = json.dump(dados, meu_json)
                                    # Compactando arquivos após alterção
                                    shutil.make_archive(f"{path}/{arquivo.replace('.zip', '')}", 'zip', f"{path}/{arquivo.replace('.zip', '')}")
                                    shutil.rmtree(f"{path}/{arquivo.replace('.zip', '')}")
                                except:
                                    pass
                except patoolib.util.PatoolError:
                    pass
        # Organizar por clientes
        clientes = ['Duplo Faturamento', 'GED', 'Fatura TWM']
        for i in clientes:
            Automacao.organizarcliente(self, i)
        
        print('FIM')
#Automacao()
