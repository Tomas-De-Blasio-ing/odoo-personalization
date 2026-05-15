{
    'name': 'Puntaje desempenio docente',
    'version': '1.0',
    'depends': [ #Se tienen que instalar antes ya que dependemos de ellos
        'base', 
        'hr',          # Empleados
        'mi_primer_modulo',
        'om_hr_payroll',
        'hr_contract'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_desempenio.xml',
        'views/hr_employee_public_desempenio.xml',
        'views/hr_payslip_desempenio.xml'
    ],
    'installable': True,
    'application': False,
}
