"""
HeatShield - Farmer-Centric Heatwave Monitoring and Early Warning System
Data Structures Laboratory - Lab 10
Primary data structure: Priority Queue implemented using a custom Max Heap.

This is an educational prototype. The temperature-risk thresholds below are
illustrative and should be adjusted using local, crop-specific agricultural
guidelines before real-world deployment.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional


# Illustrative thresholds for this prototype, not official heatwave criteria.
def temperature_risk(temperature: float) -> str:
    if temperature < 30:
        return "Low"
    elif temperature < 35:
        return "Moderate"
    elif temperature < 40:
        return "High"
    return "Critical"


RISK_POINTS = {
    "low": 1,
    "moderate": 2,
    "high": 3,
    "critical": 4,
}


def normalize_risk(value: str) -> str:
    """Validate and normalize a user-entered risk category."""
    cleaned = value.strip().capitalize()
    if cleaned.lower() not in RISK_POINTS:
        raise ValueError("Risk must be Low, Moderate, High, or Critical.")
    return cleaned


def calculate_priority(temp_risk: str, crop_risk: str, water_risk: str) -> int:
    """
    Convert three risk levels (1..4 each) into a prototype priority score (1..10).
    Formula: temperature points + crop points + water points - 2.
    Thus all-Low = 1 and all-Critical = 10.
    """
    total = (
        RISK_POINTS[temp_risk.lower()]
        + RISK_POINTS[crop_risk.lower()]
        + RISK_POINTS[water_risk.lower()]
    )
    return total - 2


def severity_from_score(score: int) -> str:
    if 1 <= score <= 3:
        return "Low"
    if 4 <= score <= 6:
        return "Moderate"
    if 7 <= score <= 8:
        return "High"
    return "Critical"


@dataclass
class HeatwaveAlert:
    region: str
    temperature: float
    crop_risk: str
    water_risk: str
    temperature_risk: str
    severity: str
    priority_score: int

    def display(self) -> str:
        return (
            f"Region: {self.region} | Temperature: {self.temperature:.1f} C | "
            f"Temperature Risk: {self.temperature_risk} | Crop Risk: {self.crop_risk} | "
            f"Water Risk: {self.water_risk} | Severity: {self.severity} | "
            f"Priority: {self.priority_score}/10"
        )


class MaxHeapPriorityQueue:
    """Array-based Max Heap. The alert with the largest score is at index 0."""

    def __init__(self):
        self.heap: List[HeatwaveAlert] = []

    def __len__(self) -> int:
        return len(self.heap)

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def _swap(self, first: int, second: int) -> None:
        self.heap[first], self.heap[second] = self.heap[second], self.heap[first]

    def _heapify_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent].priority_score >= self.heap[index].priority_score:
                break
            self._swap(parent, index)
            index = parent

    def _heapify_down(self, index: int) -> None:
        size = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if left < size and self.heap[left].priority_score > self.heap[largest].priority_score:
                largest = left
            if right < size and self.heap[right].priority_score > self.heap[largest].priority_score:
                largest = right

            if largest == index:
                break

            self._swap(index, largest)
            index = largest

    def insert(self, alert: HeatwaveAlert) -> None:
        self.heap.append(alert)
        self._heapify_up(len(self.heap) - 1)

    def peek_highest_priority(self) -> Optional[HeatwaveAlert]:
        return None if self.is_empty() else self.heap[0]

    def delete_max(self) -> Optional[HeatwaveAlert]:
        if self.is_empty():
            return None

        highest = self.heap[0]
        last = self.heap.pop()

        if not self.is_empty():
            self.heap[0] = last
            self._heapify_down(0)

        return highest

    def search_region(self, region: str) -> Optional[HeatwaveAlert]:
        target = region.strip().casefold()
        for alert in self.heap:
            if alert.region.casefold() == target:
                return alert
        return None

    def delete_region(self, region: str) -> Optional[HeatwaveAlert]:
        """Delete a specific region, then restore the heap property."""
        target = region.strip().casefold()

        for index, alert in enumerate(self.heap):
            if alert.region.casefold() == target:
                removed = self.heap[index]
                last = self.heap.pop()

                if index < len(self.heap):
                    self.heap[index] = last
                    parent = (index - 1) // 2 if index > 0 else None

                    if parent is not None and self.heap[index].priority_score > self.heap[parent].priority_score:
                        self._heapify_up(index)
                    else:
                        self._heapify_down(index)

                return removed

        return None

    def display_heap(self) -> List[HeatwaveAlert]:
        # Heap-array order is not necessarily fully sorted order.
        return list(self.heap)


def make_alert(region: str, temperature: float, crop_risk: str, water_risk: str) -> HeatwaveAlert:
    if not region.strip():
        raise ValueError("Region name cannot be empty.")

    crop = normalize_risk(crop_risk)
    water = normalize_risk(water_risk)
    temp_risk = temperature_risk(temperature)
    score = calculate_priority(temp_risk, crop, water)

    return HeatwaveAlert(
        region=region.strip(),
        temperature=temperature,
        crop_risk=crop,
        water_risk=water,
        temperature_risk=temp_risk,
        severity=severity_from_score(score),
        priority_score=score,
    )


def read_risk(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        try:
            return normalize_risk(value)
        except ValueError as error:
            print(error)


def add_alert(queue: MaxHeapPriorityQueue) -> None:
    print("\n--- Add Heatwave Alert ---")
    region = input("Enter region: ").strip()

    try:
        temperature = float(input("Enter temperature in Celsius: "))
        if temperature < -20 or temperature > 60:
            print("Please enter a plausible prototype temperature between -20 and 60 C.")
            return
        crop_risk = read_risk("Enter crop risk (Low/Moderate/High/Critical): ")
        water_risk = read_risk("Enter water risk (Low/Moderate/High/Critical): ")
        alert = make_alert(region, temperature, crop_risk, water_risk)

        existing = queue.search_region(region)
        if existing:
            print("An alert for this region already exists. Delete it before adding an updated alert.")
            return

        queue.insert(alert)
        print("\nAlert added successfully.")
        print(alert.display())
    except ValueError as error:
        print(f"Invalid input: {error}")


def view_highest(queue: MaxHeapPriorityQueue) -> None:
    print("\n--- Highest-Risk Region ---")
    alert = queue.peek_highest_priority()
    if alert is None:
        print("No active alerts.")
    else:
        print(alert.display())
        show_farmer_warning(alert)


def search_alert(queue: MaxHeapPriorityQueue) -> None:
    region = input("\nEnter region to search: ").strip()
    alert = queue.search_region(region)
    if alert:
        print("\nAlert found:")
        print(alert.display())
    else:
        print("Region not found.")


def delete_alert(queue: MaxHeapPriorityQueue) -> None:
    region = input("\nEnter region whose alert should be deleted: ").strip()
    removed = queue.delete_region(region)
    if removed:
        print("Alert deleted:")
        print(removed.display())
    else:
        print("No alert found for that region.")


def display_alerts(queue: MaxHeapPriorityQueue) -> None:
    print("\n--- All Heatwave Alerts (Heap Array Order) ---")
    alerts = queue.display_heap()
    if not alerts:
        print("No active alerts.")
        return

    for number, alert in enumerate(alerts, start=1):
        print(f"{number}. {alert.display()}")
    print("\nNote: Heap-array order guarantees the maximum at the root; the remaining entries are not fully sorted.")


def show_farmer_warning(alert: HeatwaveAlert) -> None:
    if alert.severity == "Critical":
        action = "Immediate preventive measures are recommended. Check irrigation and protect vulnerable crops."
    elif alert.severity == "High":
        action = "High agricultural risk. Monitor crops and water availability closely."
    elif alert.severity == "Moderate":
        action = "Moderate risk. Continue monitoring local conditions."
    else:
        action = "Low risk at present. Continue routine monitoring."

    print("\n*** FARMER WARNING ***")
    print(f"{alert.severity.upper()} HEATWAVE RISK")
    print(f"Region: {alert.region}")
    print(f"Temperature: {alert.temperature:.1f} C")
    print(f"Crop Risk: {alert.crop_risk}")
    print(f"Water Risk: {alert.water_risk}")
    print(action)


def generate_farmer_warning(queue: MaxHeapPriorityQueue) -> None:
    print("\n--- Farmer Warning ---")
    alert = queue.peek_highest_priority()
    if alert is None:
        print("No active alerts. No warning can be generated.")
    else:
        show_farmer_warning(alert)


def load_demo_data(queue: MaxHeapPriorityQueue) -> None:
    """Load the illustrative regions used in the HeatShield design proposal."""
    demo_alerts = [
        make_alert("Vidarbha", 44, "High", "High"),
        make_alert("Marathwada", 43, "High", "Moderate"),
        make_alert("Nashik", 41, "Moderate", "Moderate"),
        make_alert("Konkan", 39, "Low", "Low"),
    ]

    added = 0
    for alert in demo_alerts:
        if not queue.search_region(alert.region):
            queue.insert(alert)
            added += 1

    print(f"{added} illustrative demo alert(s) loaded.")
    print("Note: Scores are calculated by this prototype's documented formula.")


def print_menu() -> None:
    print("\n" + "=" * 58)
    print("                 HEATSHIELD")
    print(" Farmer-Centric Heatwave Monitoring and Early Warning")
    print("=" * 58)
    print("1. Add Heatwave Alert")
    print("2. Calculate / View Highest-Risk Region")
    print("3. Search Region")
    print("4. Delete Alert by Region")
    print("5. Display All Alerts")
    print("6. Generate Farmer Warning")
    print("7. Load Illustrative Demo Data")
    print("0. Exit")
    print("-" * 58)


def main() -> None:
    alerts = MaxHeapPriorityQueue()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_alert(alerts)
        elif choice == "2":
            view_highest(alerts)
        elif choice == "3":
            search_alert(alerts)
        elif choice == "4":
            delete_alert(alerts)
        elif choice == "5":
            display_alerts(alerts)
        elif choice == "6":
            generate_farmer_warning(alerts)
        elif choice == "7":
            load_demo_data(alerts)
        elif choice == "0":
            print("Thank you for using HeatShield. Exiting...")
            break
        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()
