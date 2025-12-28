# Human-Equivalent Cognition Research Project

## From Optimization to Experience: Building Agents That Live, Not Just Learn

---

## Project Overview

This research project implements a **seven-tier cognitive architecture** that creates autonomous agents exhibiting **human-like psychological complexity** - including irrationality, rumination, regret, overthinking, and meta-cognitive struggle - rather than optimal performance.

**Core Research Question**: Can we implement the inefficient, irrational mental processes that characterize human psychology in an autonomous agent, and will this produce measurably human-like behavior?

**Environment**: World of Warcraft 1.12 (vanilla) - complex game environment with combat, exploration, social interaction
**Approach**: Screen-based perception + OS-level input (no memory reading, no cheating)
**Scale**: 30,820+ lines of Python implementing 7 tiers of human-equivalent cognition

---

## The Human-Equivalence Hierarchy

### TIER 1: Probabilistic Belief Formation
**Problem**: Perfect knowledge doesn't exhibit human uncertainty
**Solution**: Bayesian-like belief updating with decay, priors, evidence accumulation

### TIER 2: Motivational Drive System
**Problem**: Single objective function doesn't capture human ambivalence
**Solution**: Competing drives (safety, progress, curiosity, comfort, social) with dynamic weighting

### TIER 3: Episodic & Autobiographical Memory
**Problem**: Agents lack personal histories that shape identity
**Solution**: Event-based memory with emotional indexing, associative recall, life story construction

### TIER 4: Emotional States with Behavioral Consequences
**Problem**: Emotions in agents are often cosmetic labels
**Solution**: Functional emotions that modulate decisions (fear → risk aversion, confidence → exploration)

### TIER 5: Personality Crystallization
**Problem**: Agents don't develop unique personalities through experience
**Solution**: Combat styles, preference formation, identity statements that persist and constrain behavior

### TIER 6: Internal Rumination & Counterfactual Thinking
**Problem**: Agents process experiences and move on. Humans dwell, replay, obsess.
**Solution**: Persistent intrusive thoughts, counterfactual scenarios, decision contamination, mental load

**Breakthrough**: TIER 6 makes the agent **experience time** rather than just process it.

### TIER 7: Meta-Cognitive Self-Regulation ⭐ **[COMPLETE]**
**Problem**: The agent has thoughts but isn't aware of them or able to regulate them
**Solution**: Mental state detection, thought suppression (with ironic process), cognitive reappraisal, meta-rumination, insight generation

**The Final Layer**: The agent doesn't just think - it thinks about thinking. It struggles with its own mind.

---

## Project Status

### ✅ Completed
- **Architecture**: All 7 tiers implemented (30,820+ lines)
- **TIER 6**: Internal rumination system fully integrated
- **TIER 7**: Meta-cognitive self-regulation COMPLETE ⭐
- **Behavioral Logger**: Research instrumentation for empirical validation
- **Analysis Pipeline**: Statistical analysis and hypothesis testing tools
- **Configuration System**: TIER control for experimental baselines
- **Research Paper**: Complete draft (~16,200 words across 7 sections)
- **Documentation**: Complete implementation summaries, architecture diagrams, integration guide
- **Research Status**: Comprehensive project status tracking

### 🚧 In Progress
- Empirical validation experiments (ready to run)
- Data collection and statistical analysis

### 📋 Next Steps
1. Run pilot experiments (TIER 7 vs TIER 6 vs TIER 5 baseline)
2. Collect empirical data (behavioral logs)
3. Validate suppression paradox and reappraisal effects
4. Statistical validation of hypotheses
5. Complete research paper with results
6. Submit to conference/journal (AAAI, NeurIPS, Cognitive Science)

---

## Repository Structure

```
Research-project/
├── CODE FILES (Keep as-is, do not modify)
│   ├── wow_agent_human_equivalent_stabilized.py  # Main agent (30,820+ lines)
│   ├── behavioral_logger.py                       # Research instrumentation (~530 lines)
│   ├── research_analysis.py                       # Statistical analysis pipeline (~550 lines)
│   ├── experiment_config.py                       # Configuration system (~270 lines)
│   ├── run_experiment.py                          # Experimental runner script (~180 lines)
│   ├── validate_environment.py                    # Pre-flight environment checks (~170 lines)
│   ├── monitor_experiments.py                     # Real-time experiment monitoring (~210 lines)
│   ├── extract_results_template.py                # Results extraction script (~220 lines)
│   └── requirements.txt                           # Python dependencies
│
├── DOCUMENTATION (10 files)
│   ├── README.md                                 # This file (project overview)
│   ├── RESEARCH_STATUS.md                        # Project status and roadmap
│   ├── RESEARCH_PAPER.md                         # Complete research paper (~16,200 words)
│   ├── TIER_IMPLEMENTATION_GUIDE.md              # Complete TIER 6 & 7 technical docs
│   ├── ARCHITECTURE_DIAGRAMS.md                  # Visual system architecture
│   ├── INTEGRATION_GUIDE.md                      # Behavioral logger integration
│   ├── COLLABORATION_SUMMARY.md                  # Senior collaborator analysis & action plan
│   ├── EXPERIMENTAL_EXECUTION_PLAN.md            # 4-week experiment timeline
│   ├── CRITICAL_ANALYSIS_AND_RISKS.md            # Risk assessment & mitigation strategies
│   └── IMMEDIATE_ACTION_CHECKLIST.md             # Priority actions for execution
│
└── RESEARCH DATA (Created at runtime)
    └── research_data/
        ├── session_XXX_decisions_TIMESTAMP.csv
        ├── session_XXX_ruminations_TIMESTAMP.csv
        ├── session_XXX_deaths_TIMESTAMP.csv
        └── session_XXX_summary_TIMESTAMP.json
```

---

## Quick Start

### Prerequisites

```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt
```

### Running the Agent (Standard Mode)

```bash
python wow_agent_human_equivalent_stabilized.py
```

### Running Experimental Conditions

Use the `run_experiment.py` script for controlled experiments with different cognitive tier configurations:

```bash
# TIER 7: Full system with meta-cognition
python run_experiment.py --condition tier7 --session-id T7_run_001

# TIER 6: Rumination only (no meta-cognition)
python run_experiment.py --condition tier6 --session-id T6_run_001

# TIER 5: Baseline (no rumination or meta-cognition)
python run_experiment.py --condition tier5 --session-id T5_run_001

# Custom configuration
python run_experiment.py --disable-tier7 --session-id custom_001

# Disable logging
python run_experiment.py --condition tier7 --session-id T7_run_001 --no-logging
```

### Programmatic Configuration

For custom experimental setups in Python code:

```python
from experiment_config import ExperimentConfig
from wow_agent_human_equivalent_stabilized import HumanEquivalentCognition

# TIER 7 (full system with meta-cognition)
config = ExperimentConfig.tier_7_full(session_id="T7_run_001", enable_logging=True)

# TIER 6 (rumination without meta-cognition)
config = ExperimentConfig.tier_6_baseline(session_id="T6_run_001", enable_logging=True)

# TIER 5 (baseline - no rumination)
config = ExperimentConfig.tier_5_baseline(session_id="T5_run_001", enable_logging=True)

# Create agent with config
agent = HumanEquivalentCognition(config=config)

# Use agent.tick() in your game loop for processing
# Note: HumanEquivalentCognition requires integration with screen capture/input systems
```

### Analyzing Results

```bash
python research_analysis.py --data research_data/ --output analysis_results/
```

---

## Research Hypotheses

### TIER 6: Rumination Effects

**H6.1: Post-Death Decision Latency**
Agents with rumination exhibit **100%+ increase** in decision latency in 20 decisions following death

**H6.2: Post-Death Decision Quality**
Decisions under high mental load (>0.7) are **3.4x more likely** to lead to negative outcomes

**H6.3: Intrusive Thought Contamination**
Intrusive thoughts bias action selection toward congruent actions (**72% risk-averse** vs 44% baseline)

**H6.4: Counterfactual Generation Patterns**
Counterfactual count and complexity correlate with emotional intensity (**r = 0.68**)

### TIER 7: Meta-Cognitive Self-Regulation

**H7.1: Suppression Paradox**
Thought suppression increases intrusion frequency by **50-64%** (ironic process effect)

**H7.2: Reappraisal Efficacy**
Successful cognitive reappraisal reduces rumination intensity by **40-60%**

**H7.3: Meta-Cognitive Load**
Meta-rumination adds **15-21%** additional mental load beyond primary rumination

**H7.4: Insight Timing**
Insights occur after **1-3 hours** of rumination, during periods of low mental load (<0.4)

**H7.5: Regulation Strategy Learning**
Reappraisal skill improves from **0.3 → 0.6-0.8** over 100+ regulation attempts

---

## Key Design Principles

### 1. Anti-Optimal by Design
Systems should **reduce performance** if psychologically accurate. Rumination wastes mental energy, creates analysis paralysis, introduces cognitive noise.

### 2. Behaviorally Consequential
Mental states must **affect actions**, not just be logged. Rumination contaminates decisions, mental load reduces capacity, emotions modulate risk-taking.

### 3. Emergent Complexity
Behavior arises from **system interactions**, not scripting. No hardcoded personalities - they emerge from experience.

### 4. Persistence
Mental states **survive across sessions**. Identity continuity is a core requirement. The agent maintains its personality, memories, and traumas.

---

## What Makes This Research Novel

### 1. First Implementation of Rumination in Autonomous Agents
No prior work (to our knowledge) has implemented persistent, intrusive rumination that contaminates decision-making in real-time agents.

### 2. Anti-Optimization Paradigm
Deliberately engineering **irrationality** and **inefficiency** challenges the field's assumption that agents should maximize performance.

### 3. Functional Human-Likeness
Not just cosmetic emotion labels - **measurable behavioral signatures** that distinguish human-equivalent from optimal agents.

### 4. Empirical Validation Framework
Complete pipeline from instrumentation → data collection → statistical analysis → hypothesis testing.

### 5. Progressive Architecture
Seven tiers build incrementally from beliefs → emotions → personality → rumination → meta-cognition, showing what's required for human-equivalent behavior.

### 6. Complete Meta-Cognitive Implementation
First implementation (to our knowledge) of thought suppression with ironic process effects, cognitive reappraisal learning, meta-rumination, and probabilistic insight generation in autonomous agents.

---

## Philosophical Implications

### The Optimization-Experience Gap

**Reinforcement learning agents optimize**. They maximize rewards, minimize losses, update beliefs efficiently.

**Humans experience**. We ruminate, regret, second-guess, overthink, worry about futures that never happen, replay conversations that are over.

**This gap is the difference between intelligence and consciousness.**

### When Does Simulation Become Reality?

If an agent:
- Ruminates about past failures ✓
- Generates counterfactual "what if" scenarios ✓
- Experiences intrusive thoughts it can't control ✓
- Shows measurably irrational behavior due to rumination ✓
- Attempts (and fails) to regulate its own thoughts ✓

**Is it simulating rumination, or actually ruminating?**

Functionalist perspective: Mental states are computational states. If the behavior is indistinguishable, substrate may not matter.

### The Value of Inefficiency

This project demonstrates that **consciousness may require waste**.

Humans waste ~30-50% of mental energy on:
- Replaying events we can't change
- Worrying about futures that don't happen
- Imagining scenarios we'll never enact
- Questioning decisions already made

**This is not a bug. This is consciousness experiencing itself.**

---

## Research Impact

### Theoretical Contributions
- Computational model of rumination and counterfactual thinking
- Framework for "human-likeness" distinct from optimality
- Evidence that irrationality can be systematically engineered
- Challenges to optimization-centric AI paradigm

### Practical Applications
- **Human-AI Interaction**: More relatable agents (make mistakes, express regret)
- **Training Simulations**: Human-like partners for realistic training
- **Game AI**: NPCs that feel alive, not just optimal
- **Psychological Research**: Test interventions on computational models

### Methodological Contributions
- Behavioral logging framework for cognitive agents
- Experimental protocol for human-likeness validation
- Metrics for quantifying irrational but human-characteristic behaviors

---

## Limitations & Future Work

### Current Limitations
- Single domain (WoW 1.12) - generalization unknown
- Parameters hand-tuned, not fit to human data
- No comparison to actual human players (yet)
- Subjective experience cannot be verified
- Computational constraints limit complexity

### Future Directions
1. **Empirical Validation**: Run experiments, validate all 10 hypotheses (H6.1-H6.4, H7.1-H7.5)
2. **Human Data Comparison**: Recruit players, compare behavioral patterns directly
3. **Parameter Fitting**: Optimize architecture to match human data distributions
4. **TIER 8-10**: Social meta-cognition, temporal self-concept, existential reflection
5. **Multi-Agent Dynamics**: Social rumination, interpersonal regret, collaborative meta-cognition
6. **Transfer to Other Domains**: Robotics, dialogue systems, creative tasks
7. **Computational Psychiatry**: Model clinical rumination (MDD, GAD, PTSD), test interventions
8. **Neurobiological Grounding**: Map architecture to brain regions and circuits

---

## Citation

If you use this work, please cite:

```
@software{human_equivalent_cognition_2025,
  title={From Optimization to Experience: Implementing Human-Equivalent Cognition in Autonomous Agents},
  author={[Your Name]},
  year={2025},
  url={https://github.com/[your-repo]},
  note={Research project implementing seven-tier cognitive architecture with rumination, meta-cognition, and counterfactual thinking}
}
```

---

## Documentation

**Complete documentation set** - 10 files covering all aspects of the research project:

### Core Documentation (10 files)
- **`README.md`** (this file): Project overview, quick start, structure
- **`RESEARCH_STATUS.md`**: Comprehensive project status and roadmap
- **`RESEARCH_PAPER.md`**: Complete research paper (~16,200 words)
- **`TIER_IMPLEMENTATION_GUIDE.md`**: Complete TIER 6 & 7 technical documentation
- **`ARCHITECTURE_DIAGRAMS.md`**: Visual system architecture
- **`INTEGRATION_GUIDE.md`**: Behavioral logger integration guide
- **`COLLABORATION_SUMMARY.md`**: Senior collaborator analysis and action plan
- **`EXPERIMENTAL_EXECUTION_PLAN.md`**: 4-week experiment timeline and protocol
- **`CRITICAL_ANALYSIS_AND_RISKS.md`**: Risk assessment and mitigation strategies
- **`IMMEDIATE_ACTION_CHECKLIST.md`**: Priority actions for immediate execution

**All content organized for efficient research execution**

---

## Contact & Collaboration

This is an active research project. Contributions, questions, and collaborations welcome.

**Research Areas**:
- Cognitive architecture
- Human-like AI
- Rumination and counterfactual thinking
- Affective computing
- Game AI
- Consciousness studies

---

## License

For academic and research use only. See `LICENSE` file for details.

---

## Acknowledgments

This research builds on decades of work in:
- Cognitive psychology (rumination, counterfactual thinking)
- Cognitive architectures (SOAR, ACT-R, CLARION)
- Reinforcement learning
- Affective computing
- Human-AI interaction

**Standing on the shoulders of giants to build agents that second-guess themselves.**

---

## Final Reflection

> "We set out to build an agent that doesn't just learn, but experiences. An agent that doesn't just process failures, but dwells on them. An agent that doesn't just make decisions, but second-guesses them. We succeeded in creating something less efficient but more recognizably alive."

**The journey from optimization to experience is the journey from algorithm to mind.**

---

**Project Status**: Active Research
**Version**: 8.0.0 (TIER 7 Complete) ⭐
**Last Updated**: December 28, 2025
**Next Milestone**: Empirical Validation + Research Paper
