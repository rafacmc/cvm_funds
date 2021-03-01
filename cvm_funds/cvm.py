import pandas as pd
import requests
import io, re

from datetime import date, timedelta, datetime

class FundsReport:

    def __init__(self, report, init_date, end_date):

        self.init_date = str(init_date)
        self.end_date = str(end_date)

        def report_data(report):
            switcher = {
                "INFORME_DIARIO": "DOC/INF_DIARIO/DADOS/inf_diario_fi",
                "informe_diario": "DOC/INF_DIARIO/DADOS/inf_diario_fi",
                "informe_fundos": "DOC/INF_DIARIO/DADOS/inf_diario_fi",
                "diario": "DOC/INF_DIARIO/DADOS/inf_diario_fi",
                "daily_funds": "DOC/INF_DIARIO/DADOS/inf_diario_fi",
                "daily": "DOC/INF_DIARIO/DADOS/inf_diario_fi",
                "PERFIL_FUNDOS": "DOC/PERFIL_MENSAL/DADOS/perfil_mensal_fi",
                "perfil_fundos": "DOC/PERFIL_MENSAL/DADOS/perfil_mensal_fi",
                "perfil": "DOC/PERFIL_MENSAL/DADOS/perfil_mensal_fi",
                "funds_profile": "DOC/PERFIL_MENSAL/DADOS/perfil_mensal_fi",
                "profile": "DOC/PERFIL_MENSAL/DADOS/perfil_mensal_fi",
                "CADASTRO": "CAD/DADOS/inf_cadastral_fi",
                "cadastro_fundos": "CAD/DADOS/inf_cadastral_fi",
                "cadastro": "CAD/DADOS/inf_cadastral_fi",
                "funds_register": "CAD/DADOS/inf_cadastral_fi",
                "register": "CAD/DADOS/inf_cadastral_fi"
            }

            return switcher.get(report, "Invalid argument.")

        self.active_report = report_data(str(report))

        def get_date(url_date):
            dt = url_date.split("-")
            year = dt[0]
            month = dt[1]
            return year+month

        if get_date(self.init_date) == get_date(self.end_date):

            try:
                url = "http://dados.cvm.gov.br/dados/FI/"+str(self.active_report)+"_"+str(get_date(self.end_date))+".csv"
                request = requests.get(url)
                data = io.StringIO(request.text)
                self.df = pd.read_csv(data, ";")
            except:
                raise TypeError("No data available for the specified search criteria.")

        elif get_date(self.init_date) != get_date(self.end_date):

            self.date_list = pd.date_range(self.init_date, self.end_date, freq="M").to_pydatetime().tolist()
            if self.active_report != "CAD/DADOS/inf_cadastral_fi":
                self.url_date = [datetime.strftime(dt, "%Y%m") for dt in self.date_list]
            else:
                self.url_date = [datetime.strftime(dt, "%Y%m%d") for dt in self.date_list]

            dict_data = {}

            try:
                for date_request in self.url_date:
                    url_request = requests.get("http://dados.cvm.gov.br/dados/FI/"+str(self.active_report)+"_"+str(date_request)+".csv")
                    data = io.StringIO(url_request.text)
                    dict_data[date_request] = pd.read_csv(data, ";", error_bad_lines=False)
                    self.df = pd.concat(dict_data, ignore_index=True)
            except:
                raise TypeError("No data available for the specified search criteria. Try using date greater than "+self.init_date+".")

        self.df.drop(list(self.df.filter(regex="<!DOCTYPE")), axis=1, inplace=True)


    def filter(self, cnpj_list=[]):

        if self.active_report != "CAD/DADOS/inf_cadastral_fi":
            if not cnpj_list:
                return self.df[(self.df["DT_COMPTC"] >= self.init_date)&(self.df["DT_COMPTC"] <= self.end_date)].set_index("CNPJ_FUNDO")
            else:
                if isinstance(cnpj_list, list):
                    return self.df[(self.df["DT_COMPTC"] >= self.init_date)&(self.df["DT_COMPTC"] <= self.end_date)&(self.df["CNPJ_FUNDO"].isin(cnpj_list))].set_index("CNPJ_FUNDO")
                else:
                    raise TypeError("'cnpj_list' parameter must be a list.")
        else:
            if not cnpj_list:
                return self.df.set_index("CNPJ_FUNDO")
            else:
                return self.df[self.df["CNPJ_FUNDO"].isin(cnpj_list)].set_index("CNPJ_FUNDO")
