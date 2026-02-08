import time

def sample_vessel_positions():
    """
    Returns list of vessel dicts with id, name, type, and path positions
    """
    vessels = [
        {
            'id': 'V-101', 
            'name': 'Sea Hawk',
            'type': 'fishing',
            'positions': [
                (76.15, 9.95), (76.16, 9.96), (76.17, 9.97), (76.18, 9.98), (76.19, 9.99)
            ]
        },
        {
            'id': 'V-102', 
            'name': 'Ocean Star',
            'type': 'trawler',
            'positions': [
                (76.18, 10.05), (76.185, 10.04), (76.19, 10.03), (76.195, 10.02), (76.20, 10.01)
            ]
        },
        {
            'id': 'V-103', 
            'name': 'Delta X',
            'type': 'patrol',
            'positions': [
                (76.22, 9.92), (76.21, 9.93), (76.20, 9.94), (76.19, 9.95), (76.18, 9.96)
            ]
        }
    ]
    return vessels

def get_positions_at_step(vessels, step):
    pts = []
    for v in vessels:
        # Loop functionality
        pos = v['positions'][step % len(v['positions'])]
        pts.append({
            'id': v['id'], 
            'name': v['name'],
            'type': v['type'],
            'lon': pos[0], 
            'lat': pos[1]
        })
    return pts
