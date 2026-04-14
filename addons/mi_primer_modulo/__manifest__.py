{
    'name': 'Personalizacion Ministerio',
    'version': '1.0',
    'depends': [
        'base', 
        'hr',          # Empleados
        'hr_contract', # Contratos
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/titulos_views.xml',
        'reports/titulo_reports.xml'
    ],
    'installable': True,
    'application': True,
}
