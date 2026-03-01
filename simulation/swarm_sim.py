import math
import time
import threading

class Drone:
    def __init__(self, drone_id, x, y):
        self.id = drone_id
        self.x = x
        self.y = y
        self.status = "idle"        # idle, en_route, suppressing, returning
        self.battery = 100
        self.payload = 100          # fire suppressant %
        self.target = None

    def distance_to(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def move_towards(self, tx, ty, speed=2):
        dx = tx - self.x
        dy = ty - self.y
        dist = self.distance_to(tx, ty)
        if dist < speed:
            self.x, self.y = tx, ty
        else:
            self.x += (dx / dist) * speed
            self.y += (dy / dist) * speed
        self.battery -= 0.1

    def suppress(self):
        if self.payload > 0:
            self.payload -= 5
            print(f"  [Drone {self.id}] Suppressing fire. Payload: {self.payload:.0f}%")
            return True
        return False

    def __repr__(self):
        return (f"Drone(id={self.id}, pos=({self.x:.1f},{self.y:.1f}), "
                f"status={self.status}, battery={self.battery:.0f}%, payload={self.payload:.0f}%)")


class SwarmCoordinator:
    def __init__(self, num_drones=5):
        # Spawn drones at random positions
        import random
        self.drones = [
            Drone(i, random.randint(0, 100), random.randint(0, 100))
            for i in range(num_drones)
        ]
        self.active_fires = []
        self.lock = threading.Lock()

    def dispatch_nearest(self, fire_location):
        """Dispatch the nearest available drone to a fire location."""
        fx, fy = fire_location
        with self.lock:
            available = [d for d in self.drones if d.status == "idle" and d.payload > 0]
            if not available:
                print("[WARNING] No available drones!")
                return None

            nearest = min(available, key=lambda d: d.distance_to(fx, fy))
            nearest.status = "en_route"
            nearest.target = fire_location
            self.active_fires.append(fire_location)

            print(f"[COORDINATOR] Dispatching Drone {nearest.id} to fire at {fire_location}")
            print(f"  Distance: {nearest.distance_to(fx, fy):.1f} units")
            print(f"  ETA: ~{nearest.distance_to(fx, fy) / 2:.1f} steps")

            threading.Thread(target=self._run_drone, args=(nearest,), daemon=True).start()
            return nearest

    def dispatch_swarm(self, fire_location, num=3):
        """Dispatch multiple drones to a large fire."""
        fx, fy = fire_location
        with self.lock:
            available = sorted(
                [d for d in self.drones if d.status == "idle" and d.payload > 0],
                key=lambda d: d.distance_to(fx, fy)
            )[:num]

        print(f"[COORDINATOR] Dispatching swarm of {len(available)} drones to {fire_location}")
        for drone in available:
            drone.status = "en_route"
            drone.target = fire_location
            threading.Thread(target=self._run_drone, args=(drone,), daemon=True).start()

    def _run_drone(self, drone):
        """Simulate drone flight and suppression."""
        tx, ty = drone.target
        print(f"[Drone {drone.id}] En route to ({tx}, {ty})")

        while drone.distance_to(tx, ty) > 2:
            drone.move_towards(tx, ty)
            time.sleep(0.1)

        drone.status = "suppressing"
        print(f"[Drone {drone.id}] Arrived at fire. Beginning suppression.")

        for _ in range(5):
            if not drone.suppress():
                print(f"[Drone {drone.id}] Payload depleted. Returning to base.")
                break
            time.sleep(0.5)

        drone.status = "returning"
        drone.target = (0, 0)
        drone.move_towards(0, 0)
        drone.status = "idle"
        print(f"[Drone {drone.id}] Returned to base and ready.")

    def status_report(self):
        print("\n=== SWARM STATUS ===")
        for drone in self.drones:
            print(f"  {drone}")
        print("====================\n")


if __name__ == "__main__":
    coord = SwarmCoordinator(num_drones=5)
    coord.status_report()

    print("\n[SIM] Fire detected at (50, 60)!")
    coord.dispatch_nearest((50, 60))
    time.sleep(1)

    print("\n[SIM] Large fire detected at (80, 20)!")
    coord.dispatch_swarm((80, 20), num=3)
    time.sleep(2)

    coord.status_report()
