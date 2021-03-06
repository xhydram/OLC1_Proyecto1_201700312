from AnalizadorRMT.Token import *
import os

class AnalizadorLexicoRMT:

    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.lexema = ""
        self.estado = 0
        self.linea = 1
        self.columna = 1
        self.entradaLimpia = ""
    #END -----

    def __agregarToken(self, tipoToken):
        self.entradaLimpia += self.lexema
        self.listaTokens.append(Token(tipoToken, self.lexema, self.linea, self.columna))
        self.estado = 0
        self.lexema = ""
    #END -----

    def __agregarErrorLexico(self, mensaje):
        self.listaErrores.append(mensaje)
        self.estado = 0
        self.lexema = ""
    #END -----

    def analizarCadena(self, cadena):
        cadenaEntrada = cadena + "#"
        col = 0
        i = 0

        while i < len(cadenaEntrada):
            caracterActual = cadenaEntrada[i]

            if caracterActual == '\n':
                self.linea += 1
                col = 0

            if self.estado == 0:
                if caracterActual.isalpha() or caracterActual == '_':
                    self.lexema += caracterActual
                    self.estado = 1
                    self.columna = col
                elif caracterActual.isdigit():
                    self.lexema += caracterActual
                    self.estado = 2
                    self.columna = col
                elif caracterActual == '(':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.PARENTESIS_IZQ)
                elif caracterActual == ')':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.PARENTESIS_DER)
                elif caracterActual == '+':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.SUMA)
                elif caracterActual == '-':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.RESTA)
                elif caracterActual == '/':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.DIVISION)
                elif caracterActual == '*':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.MULTIPLICACION)
                else:
                    if caracterActual == '#' and i == len(cadenaEntrada) - 1:
                        print(">>>>>>>>>>>> Fin del Analisis Lexico <<<<<<<<<<<<<")
                    elif caracterActual in ('\n',' ', '\t'):
                        self.entradaLimpia += caracterActual
                        self.estado = 0
                        self.lexema = ""
                    else:
                        self.__agregarErrorLexico("El caracter {} no es reconocido dentro del lenguaje".format(caracterActual))
            elif self.estado == 1:
                if caracterActual.isalnum() or caracterActual == '_':
                    self.lexema += caracterActual
                    self.estado = 1
                else:
                    self.__agregarToken(TipoToken.VARIABLE)
                    i -= 1
            elif self.estado == 2:
                if caracterActual.isdigit():
                    self.lexema += caracterActual
                    self.estado = 2
                elif caracterActual == '.':
                    self.lexema += caracterActual
                    self.estado = 3
                else:
                    self.__agregarToken(TipoToken.NUMERO)
                    i -= 1
            elif self.estado == 3:
                if caracterActual.isdigit():
                    self.lexema += caracterActual
                    self.estado = 4
                else:
                     self.__agregarErrorLexico("El caracter {} no es reconocido dentro del lenguaje, se esperaba un digito en {}".format(caracterActual, self.lexema)) 
            elif self.estado == 4:
                if caracterActual.isdigit():
                    self.lexema += caracterActual
                    self.estado = 4
                else:
                    self.__agregarToken(TipoToken.NUMERO)
                    i -= 1

            i += 1
            col += 1

    #END -----

    def analizarArchivo(self, ruta):  
        if os.path.isfile(ruta):
            archivo = open(ruta, "r")
            self.analizarCadena(archivo.read())
            archivo.close()
    #END
    
    def imprimirTokens(self):
        for token in self.listaTokens:
            print("=====================================================")
            print('TOKEN => {}     LEXEMA => {}'.format(token.getTipo(), token.lexema))
            print("=====================================================")
    #END

    def imprimirErrores(self):
        for error in self.listaErrores:
            print("\n\n;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
            print(error)
            print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
    #END

    def __verificarDirectorioReportes(self):
        if not os.path.isdir("reportes/"):
            os.mkdir("reportes/")

    def generarReporteErrores(self):
        self.__verificarDirectorioReportes()

        file = open("reportes/erroresrmt.html", "w")
        file.write("<!DOCTYPE html>\n<html>\n")
        file.write("<head>\n")
        file.write("    <meta charset=\"UTF-8\">\n")
        file.write("    <title>Reporte de Errores RMT</title>\n")
        file.write("    <style>")
        file.write("        *{margin:0; padding:0; box-sizing: border-box;}\n")
        file.write("        menu{background: rgb(27,38,68);text-align:center;padding:20px 0;}\n")
        file.write("        a{margin: 0 30px; text-decoration:none; font-size:20px; color:white;}\n")
        file.write("        a:hover{text-decoration: underline;}\n")
        file.write("        h1{text-align: center; margin: 30px 0;}\n")
        file.write("        table{border-collapse: collapse; margin: 0 auto; width: 40%;}\n")
        file.write("        td, th{border: 1px solid black; padding: 10px;}\n")
        file.write("       th{background: black; color: white}\n")
        file.write("    </style>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("    <menu>\n")
        file.write("        <a href=\"tokensrmt.html\">Reporte Tokens</a>\n")
        file.write("        <a href=\"erroresrmt.html\">Reporte Errores</a>\n")
        file.write("    </menu>\n")
        file.write("    <h1>Reporte de Errores Lexicos RMT</h1>\n")
        file.write("    <table>\n")
        file.write("        <thead>\n")
        file.write("            <tr>\n")
        file.write("                <th>#</th>\n")
        file.write("                <th>Error</th>\n")
        file.write("            </tr>\n")
        file.write("        </thead>\n")
        file.write("        <tbody>")

        if len(self.listaErrores) != 0:
            i = 1
            for error in self.listaErrores:
                file.write("            <tr>")
                file.write("                <td>{}</td>".format(i))
                file.write("                <td>{}</td>".format(error))
                file.write("            </tr>")
                i += 1
        else:
            file.write("            <tr>")
            file.write("                <td>0</td>")
            file.write("                <td>El archivo no tiene errores lexico :D</td>")
            file.write("            </tr>")

        file.write("        </tbody>")
        file.write("    </table>\n")
        file.write("</body>\n")
        file.write("</html>")
        file.close()

        self.__generarReporteTokens()

        os.system("start ./reportes/erroresrmt.html")
    #END

    def __generarReporteTokens(self):
        self.__verificarDirectorioReportes()

        file = open("reportes/tokensrmt.html", "w")
        file.write("<!DOCTYPE html>\n<html>\n")
        file.write("<head>\n")
        file.write("    <meta charset=\"UTF-8\">\n")
        file.write("    <title>Reporte de Tokens RMT</title>\n")
        file.write("    <style>")
        file.write("        *{margin:0; padding:0; box-sizing: border-box;}\n")
        file.write("        menu{background: rgb(27,38,68);text-align:center;padding:20px 0;}\n")
        file.write("        a{margin: 0 30px; text-decoration:none; font-size:20px; color:white;}\n")
        file.write("        a:hover{text-decoration: underline;}\n")
        file.write("        h1{text-align: center; margin: 30px 0;}\n")
        file.write("        table{border-collapse: collapse; margin: 0 auto; width: 40%;}\n")
        file.write("        td, th{border: 1px solid black; padding: 10px;}\n")
        file.write("       th{background: black; color: white}\n")
        file.write("    </style>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("    <menu>\n")
        file.write("        <a href=\"tokensrmt.html\">Reporte Tokens</a>\n")
        file.write("        <a href=\"erroresrmt.html\">Reporte Errores</a>\n")
        file.write("    </menu>\n")
        file.write("    <h1>Reporte de Tokens RMT</h1>\n")
        file.write("    <table>\n")
        file.write("        <thead>\n")
        file.write("            <tr>\n")
        file.write("                <th>#</th>\n")
        file.write("                <th>Token</th>\n")
        file.write("                <th>Lexema</th>\n")
        file.write("                <th>Fila</th>\n")
        file.write("                <th>Columna</th>\n")
        file.write("            </tr>\n")
        file.write("        </thead>\n")
        file.write("        <tbody>")

        if len(self.listaTokens) != 0:
            i = 1
            for token in self.listaTokens:
                file.write("            <tr>")
                file.write("                <td>{}</td>".format(i))
                file.write("                <td>{}</td>".format(token.getTipo()))
                file.write("                <td>{}</td>".format(token.lexema))
                file.write("                <td>{}</td>".format(token.linea))
                file.write("                <td>{}</td>".format(token.columna))
                file.write("            </tr>")
                i += 1
        else:
            file.write("            <tr>")
            file.write("                <td>0</td>")
            file.write("                <td>El archivo no tiene tokens :D</td>")
            file.write("            </tr>")

        file.write("        </tbody>")
        file.write("    </table>\n")
        file.write("</body>\n")
        file.write("</html>")
        file.close()
    #END