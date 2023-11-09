import Spezma_CV as Spezma_CV


async def main():
    my_boot = Spezma_CV.Boot
    await Spezma_CV.Boot.open(self=my_boot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
