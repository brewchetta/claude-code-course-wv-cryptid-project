"""Load the six case files. Safe to re-run: existing codes are updated in place.

    python -m app.seed
"""

import asyncio

from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.config import settings
from app.models import DOCUMENT_MODELS, Cryptid

CRYPTIDS = [
    dict(code="WV-001", name="MOTHMAN", short="MOTHMAN", klass="WINGED HUMANOID",
         county="MASON COUNTY", county_short="Mason Co.",
         description="Man-sized figure with vast wings and glowing red eyes. Seen over the old TNT area outside Point Pleasant.",
         first_report="Nov 15, 1966 — Point Pleasant"),
    dict(code="WV-002", name="FLATWOODS MONSTER", short="FLATWOODS", klass='VISITOR // "BRAXXIE"',
         county="BRAXTON COUNTY", county_short="Braxton Co.",
         description="Towering spade-headed figure in a hilltop clearing, trailing a hissing, foul-smelling mist.",
         first_report="Sep 12, 1952 — Flatwoods"),
    dict(code="WV-003", name="INDRID COLD", short="INDRID COLD", klass="THE GRINNING MAN",
         county="WOOD COUNTY", county_short="Wood Co.",
         description="A smiling stranger who stopped a motorist on the highway and spoke without moving his lips.",
         first_report="Nov 2, 1966 — near Parkersburg"),
    dict(code="WV-004", name="GRAFTON MONSTER", short="GRAFTON", klass="HEADLESS UPRIGHT",
         county="TAYLOR COUNTY", county_short="Taylor Co.",
         description="Pale, headless, upright shape seen along the riverbank road at night.",
         first_report="Jun 1964 — Grafton"),
    dict(code="WV-005", name="SHEEPSQUATCH", short="SHEEPSQUATCH", klass="HORNED CRYPTID",
         county="BOONE COUNTY", county_short="Boone Co.",
         description="Woolly, horned, bear-sized creature that walks upright and reeks of sulfur.",
         first_report="1990s — Boone County"),
    dict(code="WV-006", name="OGUA", short="OGUA", klass="RIVER ENTITY",
         county="MONONGAHELA RIVER", county_short="Monongahela R.",
         description="Massive two-headed, turtle-like river beast said to drag deer into the water.",
         first_report="Frontier-era folklore"),
]


async def main() -> None:
    client = AsyncMongoClient(settings.mongo_uri)
    await init_beanie(database=client[settings.mongo_db], document_models=DOCUMENT_MODELS)
    for row in CRYPTIDS:
        existing = await Cryptid.find_one(Cryptid.code == row["code"])
        if existing:
            await existing.set(row)
        else:
            await Cryptid(**row).insert()
    print(f"seeded {len(CRYPTIDS)} case files into {settings.mongo_db}")
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
