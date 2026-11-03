<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:output method="html" encoding="UTF-8"/>

    <xsl:template match="/">

        <html>

            <head>

                <meta charset="UTF-8"/>

                <title>Processos</title>

                <style>

                    body {
                        font-family: Arial, sans-serif;
                        background: #f2f2f2;
                        margin: 30px;
                    }

                    h1 {
                        text-align: center;
                    }

                    .processo {
                        background: white;
                        padding: 20px;
                        margin-bottom: 25px;
                        border-radius: 8px;
                    }

                    .processo h2 {
                        margin-top: 0;
                    }

                    .envolvido {
                        margin-bottom: 8px;
                    }

                    .movimentacao {
                        margin-bottom: 12px;
                    }

                </style>

            </head>

            <body>

                <h1>Processos</h1>

                <xsl:for-each select="processos/processo">

                    <div class="processo">

                        <h2>
                            Processo:
                            <xsl:value-of select="Processo"/>
                        </h2>

                        <p>
                            <strong>Data de autuação:</strong>
                            <xsl:value-of select="Data_de_autuação"/>

                        </p>

                        <h3>Envolvidos</h3>

                        <xsl:for-each select="Envolvidos/item">

                            <div class="envolvido">

                                <strong>
                                    <xsl:value-of select="name(*)"/>
                                </strong>

                                <xsl:text>: </xsl:text>

                                <xsl:value-of select="*"/>

                                <xsl:if test="not(*)">

                                    <xsl:value-of select="."/>

                                </xsl:if>

                            </div>

                        </xsl:for-each>


                        <h3>Movimentações</h3>

                        <xsl:for-each select="Movimentações/item">

                            <div class="movimentacao">

                                <strong>
                                    <xsl:value-of select="data"/>
                                </strong>

                                <xsl:text> - </xsl:text>

                                <xsl:value-of select="texto"/>

                            </div>

                        </xsl:for-each>

                    </div>

                </xsl:for-each>

            </body>

        </html>

    </xsl:template>

</xsl:stylesheet>