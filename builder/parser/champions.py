
import requests
import bs4
import click


class Champions:
    champs = {}

    def __init__(self):
        base_url = "https://www.mobafire.com/league-of-legends/champions"
        res = requests.get(base_url)

        if not res.status_code in range(200,299):
            print("Page is unreachable with code: ", res.status_code)

        soup = bs4.BeautifulSoup(res.text,"lxml")
        champ_list = soup.select(".champ-list__item.visible")
        for champ in champ_list:
            dict1 = {}
            champ_pos = champ.select(".champ-list__item__role")[0].span
            champ_name = champ.select(".champ-list__item__name")[0].b.text.lower()
            champ_link = "https://www.mobafire.com" + champ["href"]
            champ_wr = champ.select(".sort-value-winP")[0].text
            champ_pr = champ.select(".sort-value-pickP")[0].text
            dict1 = {
                champ_name: {
                    "pos":[pos.text for pos in champ_pos],
                    "win_rate": champ_wr,
                    "pick_rate": champ_pr,
                    "link":champ_link,
                }
            }
            self.champs.update(dict1)


    def query_by_name(self,name):
        champ_list = self.champs
        name_list = []
        for k,v in champ_list.items():
            if name in k:
                name_list.append({k:v})
        return name_list


    def query_by_pos(self,position):
        champ_list = self.champs
        pos_list = []
        for k,v in champ_list.items():
            if position in v["pos"]:
                pos_list.append(k.title())
        return pos_list


    def query_by_win_rate(self, threshold):
        champ_list = self.champs
        champ_dict = {}
        for k,v in champ_list.items():
            if float(v["win_rate"]) >= int(threshold):
                champ_dict.update({k.title(): v["win_rate"]})
        return dict(sorted(champ_dict.items(), key=lambda item: item[1], reverse=True))


    def query_by_pick_rate(self,threshold):
        champ_list = self.champs
        champ_dict = {}
        for k,v in champ_list.items():
            if float(v["pick_rate"]) >= int(threshold):
                champ_dict.update({k.title(): int(v["pick_rate"])})
        return dict(sorted(champ_dict.items(), key=lambda item: item[1], reverse=True))

    class Build:

        def __init__(self,hero_name):
            self.hero_name = hero_name
            try:
                build_url = Champions.champs[self.hero_name.lower()]["link"]
            except KeyError:
                print("Hero couldn't be found, please double check spelling. For more info go to builder builds --help")
                raise click.Abort()
            build_res = requests.get(build_url)
            if not build_res.status_code in range(200,299):
                print("Page is unreachable with code: ",build_res.status_code)
                raise click.Abort()
            self.soup = bs4.BeautifulSoup(build_res.text, "lxml")


        def get_summoner_spells(self):
            spell_list = []

            spell_el = self.soup.select(".champ-build__section__content__tab.current")[1]
            span_el = spell_el.select("a")
            for spell in span_el:
                spell_list.append(spell.span.text)
            return spell_list


        def get_runes(self):
            rune_path_list = []
            rune_fragment_list = []

            rune_el = self.soup.select(".champ-build__section__content__tab.current")[0]
            rune_paths = rune_el.select(".new-runes__title")
            for rune_path in rune_paths:
                rune_path_list.append(rune_path.text)
            rune_frag_el = rune_el.select(".new-runes__item.ajax-tooltip")
            for rune in rune_frag_el:
                if rune.span is not None:
                    rune_fragment_list.append(rune.span.text)
            runes = {
                rune_path_list[0]: [rune_fragment_list[n] for n in range(0,4)],
                rune_path_list[1]: [rune_fragment_list[n] for n in range(4,6)]
            }
            return runes


        def get_items(self):
            starting_items_list = []
            item_list = []

            starting_items_el = self.soup.select(".champ-build__section__content__tab.current")[2]
            starting_items = starting_items_el.select(".champ-build__item.tooltip-ajax")
            for starting_item in starting_items:
                starting_items_list.append(starting_item.span.text)

            core_items_el = self.soup.select(".champ-build__section__content__tab.current")[4]
            core_items = core_items_el.select("a")
            for core_item in core_items:
                item_list.append(core_item.span.text)

            boot_el = self.soup.select(".champ-build__section__content__tab.current")[5]
            boots = boot_el.span.text
            item_list.append(boots)

            lux_items_el = self.soup.select(".champ-build__section__content__tab.current")[6]
            lux_items = lux_items_el("a")
            for lux_item in lux_items:
                item_list.append(lux_item.span.text)

            items = {
                "starting_items": starting_items_list,
                "core_items": [item_list[n] for n in range(0,2)],
                "boots": item_list[2],
                "luxurious_items": [item for item in item_list[-3:]],
            }
            return items


        def get_skills(self):
            skills_dict = {}

            for n in range(1,5):
                skill = self.soup.select(".champ-build__abilities__row")[n]
                skill_key = skill.span.text
                skill_list = skill.select(".lit")
                skill_dict = {
                skill_key : [lvl["level"] for lvl in skill_list]
                }
                skills_dict.update(skill_dict)
            return skills_dict
