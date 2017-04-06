from cobra.core import Reaction


def add_exchange(model, metabolite, direction='demand', bound=1000.0,
                 prefix=None):
    """Add an exchange reaction (demand or uptake) for a given metabolite.

    Parameters
    ----------
    model : cobra.Model
        The model to add the exchange reaction to.
    metabolite : cobra.Metabolite
    direction : string, optional
        One of 'demand' for only import, 'sink' for only export or
        'exchange' for reversible export or uptake.
    bound : float, optional
        Upper and lower bound for the exchange reaction. Demand gets
        (0, bound), sink gets (-bound, 0) and exchange gets (-bound,
        bound).
    prefix : string, optional
        The prefix to use for the reaction. The default is to use 'EX_' for
        'exchange', 'DM_' for demand and 'SK_' for sink reactions.

    Returns
    -------
    cobra.Reaction
        The created exchange reaction.

    """
    exchange_types = {'demand': ('DM_', (0, bound)),
                      'sink': ('SK_', (-bound, 0)),
                      'exchange': ('EX_', (-bound, bound))}
    if direction not in list(exchange_types):
        raise ValueError('expected direction to be one of %s' %
                         str(list(exchange_types)))
    default_prefix, bounds = exchange_types[direction]
    if prefix is None:
        prefix = default_prefix
    reaction_id = str(prefix + metabolite.id)
    name = '{}_{}'.format(direction, metabolite.name)
    if reaction_id in model.reactions:
        raise ValueError("The metabolite already has an exchange reaction.")

    reaction = Reaction(id=reaction_id, name=name)
    reaction.add_metabolites({metabolite: -1})
    reaction.bounds = bounds
    model.add_reactions([reaction])
    return reaction
