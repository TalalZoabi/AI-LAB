
def compare_comparrisons(comp1, comp2):
    if comp1 is None or comp2 is None:
        return False
    
    if comp1[0] == comp2[0] and comp1[1] == comp2[1]:
        return True
    elif comp1[1] == comp2[0] and comp1[0] == comp2[1]:
        return True

    return False


