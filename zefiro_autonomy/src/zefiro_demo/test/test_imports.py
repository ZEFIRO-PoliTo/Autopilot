import unittest


class TestImports(unittest.TestCase):
    def test_demo_modules_import(self):
        import zefiro_demo.avoidance_node
        import zefiro_demo.fake_front_clearance_node
        import zefiro_demo.fake_goal_velocity_node
        import zefiro_demo.logger_node

        self.assertIsNotNone(zefiro_demo.avoidance_node.AvoidanceNode)
