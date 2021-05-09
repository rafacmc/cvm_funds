# cvm_funds
Dados dos Fundos registrados na Comissão de Valores Mobiliários - CVM.

No Jupyter Notebook comece por:

```python
%run cvm.py

cvm = FundsReport(report="informe_fundos", init_date="2020-01-31", end_date="2021-01-29")

df = cvm.filter()
```

### Relatórios dispoíveis:
- **Informe Diário** = informe_diario/informe_fundos/diario/daily/daily_funds
- **Perfil Mensal** = perfil_fundos/perfil/profile/funds_profile
- **Informação Cadastral** = cadastro_fundos/cadastro/register/funds_register

Veja alguns exemplos de uso em CVM_Fundos.ipynb.
