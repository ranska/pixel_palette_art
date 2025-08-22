# run setup only once
#
_SETUP_DONE = False

def setup():
    global _SETUP_DONE
    if _SETUP_DONE:
        return

    #  ColorSpaceRegistry._registry.clear()
    #  ColorSpaceRegistry.register("rgb", mixer_class=RGBMixer)

    print("Spec helper setup dony")
    _SETUP_DONE = True

# Lancer setup une fois au chargement
setup()
