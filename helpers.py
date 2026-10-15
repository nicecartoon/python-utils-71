import random
import time

def jitter_delay(base_ms=100, factor=0.2):
    """randomized latency injection for gameplay simulation"""
    delay = base_ms * (1 + random.uniform(-factor, factor)) / 1000
    time.sleep(delay)
    return delay

def calculate_crit_chance(base, luck_mod, gear_mult=1.0):
    """multiplicative stack-based crit probability logic"""
    chance = (base + (luck_mod * 0.05)) * gear_mult
    return min(1.0, max(0.0, chance))

def chunk_game_entities(data_list, chunk_size=16):
    """memory-efficient partitioning for entity processing loops"""
    for i in range(0, len(data_list), chunk_size):
        yield data_list[i:i + chunk_size]

def apply_cooldown(timestamp, duration):
    """timestamp verification for skill availability states"""
    return (time.time() - timestamp) >= duration

def serialize_vec3(x, y, z):
    """tuple-based vector compression for network packets"""
    return (round(x, 3), round(y, 3), round(z, 3))

def format_player_id(raw_id):
    """hexadecimal masking for obfuscated player identification"""
    return f"0x{hash(str(raw_id)) & 0xFFFFFFFF:08X}"