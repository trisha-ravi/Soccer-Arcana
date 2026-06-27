"""Aureate Arcana deck — aligned with static/deck.js and card artwork."""

ARCANA_CARDS = {
    "The Trickster": {
        "card_id": "trickster",
        "archetype": "Flair · Deception · The Unexpected",
        "symbolic_meaning": "Clever deception that turns expectation upside down.",
        "tactical_meaning": "Nutmegs, feints, and disguised passes that break defensive shape.",
        "emotional_meaning": "Gasping delight when skill humiliates the defense.",
        "cultural_meaning": "The global love of flair, from futsal streets to Neymar moments.",
    },
    "The Tower": {
        "card_id": "tower",
        "archetype": "Collapse · Exposure · Sudden Ruin",
        "symbolic_meaning": "A strong structure collapses in a single instant.",
        "tactical_meaning": "A defensive line breaks through one lost duel or bad line.",
        "emotional_meaning": "Shock as control and confidence vanish at once.",
        "cultural_meaning": "Famous late collapses that rewrite title races and legacies.",
    },
    "The Surge": {
        "card_id": "surge",
        "archetype": "Pressure · Relentlessness · The Siege",
        "symbolic_meaning": "Pressure becomes weather — wave after wave until shelter is gone.",
        "tactical_meaning": "Sustained pressing, sharp rest-defence, and recycled attacks.",
        "emotional_meaning": "Suffocation for defenders, intoxication for attackers.",
        "cultural_meaning": "German Sturm culture and the romance of relentless intensity.",
    },
    "The Chaos Card": {
        "card_id": "chaos",
        "archetype": "Controversy · Fortune · The Twist",
        "symbolic_meaning": "Order dissolves and chance takes the wheel.",
        "tactical_meaning": "VAR calls, soft penalties, scrambles, and deflections no coach can script.",
        "emotional_meaning": "Fury and elation in a single breath.",
        "cultural_meaning": "Infamous moments where rules and fortune outlive the final score.",
    },
    "The Fortress": {
        "card_id": "fortress",
        "archetype": "Defiance · Resilience · The Last Line",
        "symbolic_meaning": "The walls hold and the attack is turned away.",
        "tactical_meaning": "Compact defending, blocks, and a keeper protecting the line.",
        "emotional_meaning": "Grim pride in surviving pressure together.",
        "cultural_meaning": "Underdog resistance nights when giants cannot score.",
    },
    "The Catalyst": {
        "card_id": "catalyst",
        "archetype": "Spark · Ignition · The Turning Point",
        "symbolic_meaning": "One strike rewrites the story the match was telling.",
        "tactical_meaning": "A decisive pass, press trigger, or shot that breaks a stalemate.",
        "emotional_meaning": "Electric shock through the stadium as momentum shifts.",
        "cultural_meaning": "Every culture knows the player who will not let the moment pass.",
    },
    "The Shadow": {
        "card_id": "shadow",
        "archetype": "Hidden Threat · Eclipse · The Unseen",
        "symbolic_meaning": "Threat gathers where no one is looking.",
        "tactical_meaning": "Blind-side runs, poacher's timing, and movement off the ball.",
        "emotional_meaning": "Dread for defenders who spot the danger too late.",
        "cultural_meaning": "The fantasma, the fox in the box, the striker who decides in silence.",
    },
    "The Sun": {
        "card_id": "sun",
        "archetype": "Clarity · Triumph · The Shining Hour",
        "symbolic_meaning": "Clarity arrives and the right side shines through.",
        "tactical_meaning": "Dominant structure, crisp passing, and a plan executed cleanly.",
        "emotional_meaning": "Warm relief and joy when everything finally clicks.",
        "cultural_meaning": "The sunlit ideal of beautiful, expressive football.",
    },
    "The Engine": {
        "card_id": "engine",
        "archetype": "Tempo · Stamina · The Heartbeat",
        "symbolic_meaning": "The unseen pulse that lets the spectacular happen at all.",
        "tactical_meaning": "Box-to-box tempo, screening, recycling possession, resetting shape.",
        "emotional_meaning": "Quiet reverence for the player who covers every blade of grass.",
        "cultural_meaning": "English canonisation of the tireless midfielder.",
    },
    "The Mirror": {
        "card_id": "mirror",
        "archetype": "Symmetry · Rivalry · Reflection",
        "symbolic_meaning": "A team meets its own reflection on the pitch.",
        "tactical_meaning": "Identical structures, man-for-man canceling, one broken symmetry decides it.",
        "emotional_meaning": "Tension wound impossibly tight until the smallest crack feels seismic.",
        "cultural_meaning": "Derby fate — Boca and River, the two Milans, family feuds on grass.",
    },
    "The Wave": {
        "card_id": "wave",
        "archetype": "The Crowd · Momentum · The Twelfth Man",
        "symbolic_meaning": "Eleven players become twelve when the crowd inhales together.",
        "tactical_meaning": "Territory shifts after a roar — the home side pushes, the away side retreats.",
        "emotional_meaning": "Goosebumps made collective; belief carrying a tiring team.",
        "cultural_meaning": "The curva, the bombo, the wall of sound across football cultures.",
    },
    "The Anchor": {
        "card_id": "anchor",
        "archetype": "Anchor · Shield · The Holding Role",
        "symbolic_meaning": "Stability disguised as stillness at the base of the team.",
        "tactical_meaning": "The pivot screens channels, intercepts transitions, kills counters early.",
        "emotional_meaning": "Calm radiating outward so artists ahead play without fear.",
        "cultural_meaning": "The regista-destroyer hybrid revered as the team's keel.",
    },
}

CARD_IDS = {name: meta["card_id"] for name, meta in ARCANA_CARDS.items()}

DECK_CARD_NAMES = list(ARCANA_CARDS.keys())
