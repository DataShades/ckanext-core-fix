# ckanext-core-fix

This extensions comes to provide temprorary fixes to CKAN core that isn't yet applied, but will be (probably) applied soon.

By default, all the fixes are enabled. Check the **List of fixes** and **Config settings**
section to understand how to disabled specific fix.

All the fixes must be associated with a PR to the CKAN core.

Merged fixes could be deleted from this extension with new versions, as I don't
want to store them forever and increase the list of disabled fixes in config.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.7 and earlier             | not tested    |
| 2.8             | not tested    |
| 2.9             | not tested    |
| 2.10.0             | yes    |

## Installation

I suggest using `pip install ckanext-core-fix` to install package. If you want to install it from github, you probably know what to do.

Add `core_fix` to `ckan.plugins` to enable the plugin.

## List of fixes
Use a fix name from the parentheses to disable it via `ckanext.core_fix.disable_fix`

1. Fix dashboard activity page (`dashboard_activity`)
	Fix call of `dashboard_activity_stream` helper.
	https://github.com/ckan/ckan/pull/7482
    *Already in master*

2. Fix markdown macro regression (`markdown_macro`)
    Fix a regression of markdown.html macro after migration to bootstrap 5.
    https://github.com/ckan/ckan/pull/7485
    *Already in master*

3. Fix fontawesome icons (`fontawesome_icons`)
    Fix missing fontawesome icons after migration to bootstrap 5.
    https://github.com/ckan/ckan/pull/7474
    *Already in master*

4. Fix secondary block order (`secondary_order`)
    Fix primary/secondary order regression.
    https://github.com/ckan/ckan/pull/7468
    *Already in master*

5. Fix button icon/text gap (`button_icon_text_gap`)
    Fix missing gap between btn icon and text.
    https://github.com/ckan/ckan/pull/7470
    *Already in master*

6. Fix mobile layout breakpoint (`mobile_layout_breakpoint`)
    Fix improper breakpoint for mobile view after migration to bootstrap 5.
    https://github.com/ckan/ckan/pull/7467
    *Already in master*

7. Restyle activities (`restyle_activity`)
    Restyle activities list page in a modern way
    https://github.com/ckan/ckan/pull/7491

8. Fix group_list missing csrf (`group_list_csrf`)
    Add csrf token to a dataset group list form
    *Already in master*

8. Fix dashboard organization tab org labels and link (`dashboard_organization`)
    *Already in master*

9. Fix Redis session serialization (`redis_session`)  
   Fix serialization issues with `Markup` objects in Flask sessions.  
   Replaces default Flask-Session Redis interface with a custom implementation using `msgspec`.  
   https://github.com/ckan/ckan/pull/8704  
   *Ongoing PR in CKAN core* 

## Config settings

	# Provide a list of fixes names to disable it
	# (optional, default: None).
	ckanext.core_fix.disable_fix = dashboard_activity

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
