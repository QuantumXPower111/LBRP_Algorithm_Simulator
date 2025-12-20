import streamlit as st
import json
from enum import Enum
from dataclasses import dataclass
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from functools import lru_cache

# ==================== CONSTANTS ====================
CSS_STYLES = """
<style>
    :root {
        --keter-color: #ffffff;
        --chesed-color: #4169e1;
        --gevurah-color: #dc143c;
        --tiferet-color: #ffd700;
        --malkuth-color: #228b22;
    }
    
    .main-header {
        background: linear-gradient(90deg, #000428 0%, #004e92 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .ritual-phase-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid var(--tiferet-color);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .ritual-phase-card:hover {
        background: rgba(255, 215, 0, 0.1);
        transform: translateX(5px);
    }
    
    .vibration-text {
        animation: vibrate 0.5s linear infinite;
        font-weight: bold;
        color: #ffd700;
    }
    
    .progress-container {
        height: 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #ffd700, #ff8c00);
        transition: width 0.5s ease;
    }
</style>
"""

TREE_OF_LIFE_HTML = """
<div style='font-family: monospace; background: #000; color: #ffd700; padding: 2rem; border-radius: 10px; margin: 1rem 0; border: 1px solid #444;'>
<pre style='text-align: center; margin: 0;'>
               ╭────────── KETER ───────────╮
               │         (ATEH)              │
               │          Divine Will        │
               ╰─────────────┬──────────────╯
                             │
                             ▼
                          DA'AT
                             │
               ╭─────────────┴─────────────╮
               │                           │
               ▼                           ▼
          CHESED (Mercy)           GEVURAH (Severity)
          (VE-GEDULAH)             (VE-GEBURAH)
                             │
                             ▼
                         TIFERET (Beauty)
                             │
               ╭─────────────┴─────────────╮
               │                           │
               ▼                           ▼
            HOD (Glory)                NETZACH (Victory)
                             │
                             ▼
                         YESOD (Foundation)
                             │
                             ▼
                        MALKUTH (Kingdom)
</pre>
</div>
"""

# ==================== DATA MODELS ====================
class Direction(Enum):
    EAST = ("East", "⬟", "#87ceeb")
    SOUTH = ("South", "⬠", "#ff4500")
    WEST = ("West", "⬟", "#1e90ff")
    NORTH = ("North", "⬠", "#8b4513")
    
    def __init__(self, display_name: str, symbol: str, color: str):
        self.display_name = display_name
        self.symbol = symbol
        self.color = color

class Element(Enum):
    AIR = "Air"
    FIRE = "Fire"
    WATER = "Water"
    EARTH = "Earth"
    SPIRIT = "Spirit"

class Sephira(Enum):
    KETER = "Keter"
    CHESED = "Chesed"
    GEVURAH = "Gevurah"
    TIFERET = "Tiferet"
    MALKUTH = "Malkuth"

@dataclass
class KabbalisticEntity:
    """Data container for Kabbalistic correspondences"""
    name: str
    sephira: Sephira
    divine_name: str
    element: Element
    direction: Direction
    hebrew_letter: str = ""
    
    @property
    def color(self) -> str:
        return self.direction.color

@dataclass
class RitualStep:
    """Data container for ritual steps with serialization support"""
    phase: str
    number: int
    title: str
    description: str
    vibration: str = ""
    gesture: str = ""
    visualization: str = ""
    sephira: Optional[Sephira] = None
    html_content: str = ""
    
    def to_dict(self):
        return {
            "phase": self.phase,
            "number": self.number,
            "title": self.title,
            "description": self.description,
            "vibration": self.vibration,
            "gesture": self.gesture,
            "visualization": self.visualization,
            "sephira": self.sephira.value if self.sephira else None,
            "html_content": self.html_content
        }

# ==================== CACHED DATA ====================
@lru_cache(maxsize=1)
def get_correspondences() -> Dict[Direction, KabbalisticEntity]:
    """Cache correspondences to avoid recreation"""
    return {
        Direction.EAST: KabbalisticEntity(
            "Air", Sephira.KETER, "YHVH (יהוה)", Element.AIR, Direction.EAST, "י"
        ),
        Direction.SOUTH: KabbalisticEntity(
            "Fire", Sephira.GEVURAH, "ADONAI (אדני)", Element.FIRE, Direction.SOUTH, "ה"
        ),
        Direction.WEST: KabbalisticEntity(
            "Water", Sephira.CHESED, "EHEIEH (אהיה)", Element.WATER, Direction.WEST, "ו"
        ),
        Direction.NORTH: KabbalisticEntity(
            "Earth", Sephira.MALKUTH, "AGLA (אגלא)", Element.EARTH, Direction.NORTH, "ה"
        )
    }

@lru_cache(maxsize=1)
def get_archangels() -> Dict[Direction, Dict]:
    """Cache archangel data"""
    return {
        Direction.EAST: {
            "name": "Raphael",
            "colors": "Yellow-Purple",
            "attributes": "Healing, Wisdom, Air",
            "hebrew": "רפאל",
            "symbol": "⚗️"
        },
        Direction.SOUTH: {
            "name": "Michael",
            "colors": "Red-Green",
            "attributes": "Protection, Fire, Strength",
            "hebrew": "מיכאל",
            "symbol": "⚔️"
        },
        Direction.WEST: {
            "name": "Gabriel",
            "colors": "Blue-Orange",
            "attributes": "Strength, Water, Revelation",
            "hebrew": "גבריאל",
            "symbol": "🕊️"
        },
        Direction.NORTH: {
            "name": "Uriel",
            "colors": "Green-Brown",
            "attributes": "Light, Earth, Wisdom",
            "hebrew": "אוריאל",
            "symbol": "🔥"
        }
    }

@lru_cache(maxsize=1)
def get_cross_steps() -> List[Tuple]:
    """Cache cross ritual steps"""
    return [
        ("ATEH (אַתָּה)", "Touch forehead", "Keter - Divine Will", 
         "Visualize white light descending", Sephira.KETER),
        ("MALKUTH (מַלְכוּת)", "Point downward", "Malkuth - Kingdom", 
         "Draw light to feet, connecting heaven and earth", Sephira.MALKUTH),
        ("VE-GEBURAH (וְגבוּרָה)", "Touch right shoulder", "Gevurah - Severity/Power", 
         "Red pillar of strength", Sephira.GEVURAH),
        ("VE-GEDULAH (וְגדוּלָה)", "Touch left shoulder", "Chesed - Mercy/Glory", 
         "Blue pillar of mercy", Sephira.CHESED),
        ("LE-OLAM, AMEN (לעולם, אמן)", "Clasp hands at chest", "Tiferet - Beauty/Harmony", 
         "Golden glow at heart center", Sephira.TIFERET)
    ]

# ==================== HTML GENERATORS ====================
class HTMLGenerator:
    """Static HTML generator methods"""
    
    @staticmethod
    def generate_preparation() -> str:
        return """
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #000428 0%, #004e92 100%); color: white; border-radius: 10px;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>✡️</div>
            <h3 style='color: #ffd700;'>Preparation Phase</h3>
            <p>Microcosm aligning with Macrocosm</p>
        </div>
        """
    
    @staticmethod
    def generate_cross_step(step_num: int, vibration: str, sephira: Sephira) -> str:
        colors = {
            Sephira.KETER: "#ffffff",
            Sephira.CHESED: "#4169e1",
            Sephira.GEVURAH: "#dc143c",
            Sephira.TIFERET: "#ffd700",
            Sephira.MALKUTH: "#228b22"
        }
        color = colors.get(sephira, "#ffffff")
        
        return f"""
        <div style='border-left: 4px solid {color}; padding-left: 1rem; margin: 1rem 0;'>
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='background: {color}; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center;'>
                    {step_num}
                </div>
                <h4 style='color: {color}; margin: 0;'>{vibration.split(' ')[0]}</h4>
            </div>
            <p style='margin: 0.5rem 0;'><strong>Sephira:</strong> {sephira.value}</p>
            <p class='vibration-text' style='font-size: 1.2rem;'>{vibration}</p>
        </div>
        """
    
    @staticmethod
    def generate_pentagram(direction: Direction, entity: KabbalisticEntity, step_num: int) -> str:
        rgb = ','.join(str(int(entity.color.lstrip('#')[i:i+2], 16)) for i in (0, 2, 4))
        progress = (step_num / 4) * 100
        
        return f"""
        <div style='background: rgba({rgb}, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <div style='font-size: 3rem; color: {entity.color};'>{direction.symbol}</div>
            <h4 style='color: {entity.color};'>{direction.display_name} - {entity.element.value}</h4>
            <p><strong>Divine Name:</strong> {entity.divine_name}</p>
            <p><strong>Hebrew Letter:</strong> {entity.hebrew_letter}</p>
            <div class='progress-container'>
                <div class='progress-bar' style='width: {progress}%;'></div>
            </div>
        </div>
        """
    
    @staticmethod
    def generate_archangel(direction: Direction, archangel: Dict) -> str:
        return f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem; text-align: center; min-height: 150px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 2rem;'>{archangel['symbol']}</div>
            <h4>{archangel['name']}</h4>
            <p style='font-size: 1.5rem; margin: 0.5rem 0;'>{archangel['hebrew']}</p>
            <p><small>{archangel['attributes']}</small></p>
        </div>
        """

# ==================== MAIN SIMULATOR ====================
class LBRPSimulator:
    """Optimized LBRP simulator with lazy loading"""
    
    def __init__(self):
        self._steps = None
        self.current_step = 0
        self.ritual_type = "LBRP"
    
    @property
    def steps(self) -> List[RitualStep]:
        """Lazy load steps"""
        if self._steps is None:
            self._steps = self._generate_steps()
        return self._steps
    
    def _generate_steps(self) -> List[RitualStep]:
        """Generate ritual steps"""
        steps = []
        
        # Preparation
        steps.append(RitualStep(
            "Preparation", 1, "Centering & Intention",
            "Take three deep breaths. Visualize expanding to cosmic scale. Set intention for purification and protection.",
            visualization="White light expanding from your center",
            html_content=HTMLGenerator.generate_preparation()
        ))
        
        # Qabalistic Cross
        steps.extend(self._add_cross_phase("Qabalistic Cross", amplified=False))
        
        # Pentagrams
        correspondences = get_correspondences()
        for i, direction in enumerate(Direction, 1):
            entity = correspondences[direction]
            steps.append(RitualStep(
                "Formulating Pentagrams", len(steps) + 1,
                f"{direction.display_name} Pentagram",
                f"Drawing {entity.element.value} pentagram with divine name {entity.divine_name}",
                vibration=entity.divine_name,
                gesture="Sign of Enterer → Sign of Silence",
                visualization=f"{entity.color} flame forming pentagram",
                sephira=entity.sephira,
                html_content=HTMLGenerator.generate_pentagram(direction, entity, i)
            ))
        
        # Archangels
        archangels = get_archangels()
        positions = {
            Direction.EAST: "Before me",
            Direction.WEST: "Behind me",
            Direction.SOUTH: "On my right",
            Direction.NORTH: "On my left"
        }
        
        for direction in Direction:
            archangel = archangels[direction]
            steps.append(RitualStep(
                "Archangel Evocation", len(steps) + 1,
                f"{archangel['name']} ({archangel['hebrew']})",
                f"{positions[direction]}, {archangel['name']}: {archangel['attributes']}",
                vibration=archangel['name'],
                visualization=f"Visualize {archangel['name']} in {archangel['colors']} light",
                html_content=HTMLGenerator.generate_archangel(direction, archangel)
            ))
        
        # Closing Cross
        steps.extend(self._add_cross_phase("Closing Cross", amplified=True))
        
        return steps
    
    def _add_cross_phase(self, phase_name: str, amplified: bool) -> List[RitualStep]:
        """Generate cross phase steps"""
        steps = []
        cross_steps = get_cross_steps()
        
        for i, (vibration, gesture, sephira_desc, visualization, sephira) in enumerate(cross_steps, 1):
            vis = f"{visualization} - Amplified" if amplified else visualization
            title = f"{vibration.split(' ')[0]} (Closing)" if amplified else vibration.split(' ')[0]
            desc = f"Repeating {vibration} with enhanced resonance" if amplified else f"{sephira_desc}: {vibration}"
            
            steps.append(RitualStep(
                phase_name, len(steps) + 1, title, desc,
                vibration=vibration, gesture=gesture, visualization=vis,
                sephira=sephira,
                html_content=HTMLGenerator.generate_cross_step(i, vibration, sephira)
            ))
        
        return steps

# ==================== STREAMLIT APP ====================
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'simulator': LBRPSimulator(),
        'current_step': 0,
        'balance': [random.randint(70, 100) for _ in range(5)]
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def create_sidebar() -> None:
    """Create sidebar controls"""
    with st.sidebar:
        st.markdown("### 🎛️ Ritual Controls")
        
        # Ritual type selection
        ritual_type = st.radio(
            "Ritual Type",
            ["LBRP (Banishing)", "LIRP (Invoking)"],
            index=0
        )
        st.session_state.simulator.ritual_type = ritual_type.split(" ")[0]
        
        st.markdown("---")
        st.markdown("### 📊 Progress")
        
        # Progress display
        total_steps = len(st.session_state.simulator.steps)
        progress = (st.session_state.current_step / total_steps * 100) if total_steps else 0
        
        st.markdown(f"""
        <div class='progress-container'>
            <div class='progress-bar' style='width: {progress:.1f}%;'></div>
        </div>
        <p style='text-align: center;'>Step {min(st.session_state.current_step + 1, total_steps)} of {total_steps}</p>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("◀️ Previous", disabled=st.session_state.current_step == 0):
                st.session_state.current_step = max(0, st.session_state.current_step - 1)
                st.rerun()
        
        with col2:
            if st.button("Next ▶️", disabled=st.session_state.current_step >= total_steps - 1):
                st.session_state.current_step = min(total_steps - 1, st.session_state.current_step + 1)
                st.rerun()
        
        # Reset button
        if st.button("🔁 Reset Ritual"):
            st.session_state.current_step = 0
            st.session_state.simulator = LBRPSimulator()
            st.session_state.balance = [random.randint(70, 100) for _ in range(5)]
            st.rerun()

def render_step_content(current_step: RitualStep) -> None:
    """Render the current step content"""
    # Step header
    st.markdown(f"""
    <div class='ritual-phase-card'>
        <h3>Phase: {current_step.phase}</h3>
        <h2 style='color: #ffd700;'>{current_step.title}</h2>
        <p>{current_step.description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step details in columns
    col1, col2 = st.columns(2)
    with col1:
        if current_step.vibration:
            st.markdown("### 🔊 Vibration")
            st.markdown(f"<h2 class='vibration-text'>{current_step.vibration}</h2>", unsafe_allow_html=True)
    
    with col2:
        if current_step.gesture:
            st.markdown("### 👐 Gesture")
            st.info(current_step.gesture)
    
    # Visualization
    if current_step.visualization:
        st.markdown("### 👁️ Visualization")
        st.markdown(f"*{current_step.visualization}*")
    
    # Custom HTML content
    if current_step.html_content:
        st.markdown(current_step.html_content, unsafe_allow_html=True)
    
    # Special phase handling
    if current_step.phase == "Formulating Pentagrams":
        _render_direction_indicator()
    elif current_step.phase == "Archangel Evocation":
        _render_archangel_correspondences()

def _render_direction_indicator():
    """Render directional sequence indicator"""
    st.markdown("### 🗺️ Directional Sequence")
    cols = st.columns(4)
    for i, direction in enumerate(Direction):
        with cols[i]:
            is_active = i == (st.session_state.current_step - 6) % 4
            color = "#ffd700" if is_active else "#666"
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; border: 2px solid {color}; border-radius: 5px;'>
                <div style='font-size: 1.5rem;'>{direction.symbol}</div>
                <strong style='color: {color};'>{direction.name}</strong>
            </div>
            """, unsafe_allow_html=True)

def _render_archangel_correspondences():
    """Render archangel correspondences"""
    st.markdown("### 👼 Archangel Correspondences")
    archangel_data = {
        "Raphael": {"element": "Air", "color": "#87ceeb", "planet": "Mercury"},
        "Michael": {"element": "Fire", "color": "#ff4500", "planet": "Sun"},
        "Gabriel": {"element": "Water", "color": "#1e90ff", "planet": "Moon"},
        "Uriel": {"element": "Earth", "color": "#8b4513", "planet": "Venus"}
    }
    
    cols = st.columns(4)
    for i, (name, data) in enumerate(archangel_data.items()):
        with cols[i]:
            st.markdown(f"""
            <div style='background: {data["color"]}20; padding: 10px; border-radius: 10px; text-align: center;'>
                <h4>{name}</h4>
                <p><strong>Element:</strong> {data["element"]}</p>
                <p><strong>Planet:</strong> {data["planet"]}</p>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar_panel() -> None:
    """Render the right sidebar panel"""
    # Tree of Life
    st.markdown("### 🌳 Tree of Life")
    st.markdown(TREE_OF_LIFE_HTML, unsafe_allow_html=True)
    
    # Elemental Balance
    st.markdown("### ⚖️ Elemental Balance")
    elements = ["Air", "Fire", "Water", "Earth", "Spirit"]
    balance = st.session_state.balance
    colors = ["#87ceeb", "#ff4500", "#1e90ff", "#8b4513", "#9370db"]
    
    for element, value, color in zip(elements, balance, colors):
        st.markdown(f"""
        <div style='margin: 10px 0;'>
            <div style='display: flex; justify-content: space-between;'>
                <span>{element}</span>
                <span>{value}%</span>
            </div>
            <div class='progress-container'>
                <div class='progress-bar' style='width: {value}%; background: {color};'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Download button
    st.markdown("---")
    ritual_data = {
        "timestamp": datetime.now().isoformat(),
        "ritual_type": st.session_state.simulator.ritual_type,
        "steps_completed": st.session_state.current_step + 1,
        "steps": [step.to_dict() for step in st.session_state.simulator.steps[:st.session_state.current_step + 1]]
    }
    
    st.download_button(
        label="📥 Download Ritual Data",
        data=json.dumps(ritual_data, indent=2, default=str),
        file_name=f"lbrp_ritual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="Kabbalistic LBRP Algorithm Simulator",
        page_icon="✡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject CSS
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    
    # Initialize session state
    random.seed(42)  # For reproducible random balance
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class='main-header'>
        <h1 style='color: #ffd700; margin: 0;'>✡️ Kabbalistic LBRP Algorithm Simulator</h1>
        <p style='opacity: 0.8;'>Lesser Banishing Ritual of the Pentagram - Interactive Visualization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    create_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        simulator = st.session_state.simulator
        current_step_idx = st.session_state.current_step
        
        if current_step_idx < len(simulator.steps):
            render_step_content(simulator.steps[current_step_idx])
        else:
            # Ritual Complete
            st.markdown("""
            <div style='text-align: center; padding: 4rem; background: linear-gradient(135deg, #000428 0%, #004e92 100%); color: white; border-radius: 20px;'>
                <div style='font-size: 5rem;'>✨</div>
                <h1 style='color: #ffd700;'>Ritual Complete</h1>
                <h3>Sacred Space Established</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎯 Transformational Outputs")
            outputs = [
                "Space purified of chaotic influences",
                "Personal microcosm aligned with macrocosm",
                "Elemental forces balanced",
                "Divine protection established",
                "Inner temple created for spiritual work"
            ]
            for i, output in enumerate(outputs, 1):
                st.markdown(f"**{i}.** {output}")
    
    with col2:
        render_sidebar_panel()

if __name__ == "__main__":
    main()
