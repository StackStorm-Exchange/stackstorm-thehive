[![Exchange Template](https://exchange.stackstorm.org/assets/images/st2-logo.png)](https://exchange.stackstorm.org/)

# StackStorm Exchange Pack Template

This is a basic template directory structure for a StackStorm Integration Pack.

## How to Use

1. Clone this repository, and rename the directory to your pack name.
2. Edit `pack.yaml`. Make sure you set the pack name, the description, and add some meaningful
   keywords.
3. Add any Python dependencies to `requirements.txt`
4. Edit `config.schema.yaml`. This contains the schema for pack-specific configuration items.
5. Move `template.yaml.example` to `<pack_name>.yaml.example`, and add some example
   configuration. This will get validated against your configuration schema.
6. Add your actions, sensors and workflows. Need code ideas? Check [Github](https://github.com/StackStorm-Exchange/)!
8. Test your pack, and when it's ready, submit to [exchange-incubator](https://github.com/StackStorm-Exchange/exchange-incubator)

Any problems or questions? Check the [docs](https://docs.stackstorm.com/packs.html) or hit us up on [Slack](https://stackstorm.com/community-signup)
