import copy
import unittest
import database as db
import helpers
import config
import csv

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clientes.lista = [
            db.Cliente("15J", "Marta", "Pérez"),
            db.Cliente("48H", "Manolo", "López"),
            db.Cliente("28Z", "Ana", "Garcia"),
        ]

    def test_buscar_clientes(self):
        cliente_existente = db.Clientes.buscar("15J")
        cliente_inexistente = db.Clientes.buscar("99X")
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('39X', 'Aitor', 'Sánchez')
        self.assertEqual(4, len(db.Clientes.lista))
        self.assertEqual('39X', nuevo_cliente.dni)
        self.assertEqual('Aitor', nuevo_cliente.nombre)
        self.assertEqual('Sánchez', nuevo_cliente.apellido)

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('28Z'))
        cliente_modificado = db.Clientes.modificar('28Z', 'Mariana', 'García')
        self.assertEqual('Ana', cliente_a_modificar.nombre)
        self.assertEqual('Mariana', cliente_modificado.nombre)

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('48H')
        cliente_rebuscado = db.Clientes.buscar('48H')
        self.assertEqual(cliente_borrado.dni, '48H')
        self.assertIsNone(cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('000A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('B11', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('48H', db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('48H')
        db.Clientes.borrar('15J')
        db.Clientes.modificar('28Z', 'Mariana', 'García')

        dni, nombre, apellido  = None, None, None
        with open(config.DATABASE_PATH) as fichero:
            reader = csv.reader(fichero, delimiter=';')
            dni, nombre, apellido = next(reader)

        self.assertEqual(dni, '28Z')
        self.assertEqual(nombre, 'Mariana')
        self.assertEqual(apellido, 'García')