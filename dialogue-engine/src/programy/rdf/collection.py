"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from programy.mappings.base import BaseCollection
from programy.storage.factory import StorageFactory
from programy.utils.language.japanese import JapaneseLanguage

from datetime import datetime


class RDFEntity(object):

    def __init__(self, subject):
        self._subject = subject
        self._predicates = {}


class RDFCollection(BaseCollection):

    RDFS = "rdfs"

    def __init__(self):
        BaseCollection.__init__(self)
        self._entities = {}
        self._stores = {}
        self._entities_to_ids = {}
        self._entities_to_stores = {}
        self._load_file = False
        self._storage_factory = None
        self._update_Date = None

    @property
    def entities(self):
        return self._entities

    def empty(self):
        YLogger.debug(self, "Emptying RDF Collection")
        self._entities.clear()
        self._stores.clear()
        self._entities_to_ids.clear()
        self._entities_to_stores.clear()

    def contains(self, rdfname):
        return bool(rdfname.upper() in self._stores)

    def storename(self, mapname):
        if mapname in self._stores:
            return self._stores[mapname]
        return None

    def load(self, storage_factory):
        YLogger.debug(self, "Loading RDF Collection")
        self._load_file = True
        self._storage_factory = storage_factory
        if storage_factory.entity_storage_engine_available(StorageFactory.RDF) is True:
            rdf_engine = storage_factory.entity_storage_engine(StorageFactory.RDF)
            if rdf_engine:
                try:
                    rdfs_store = rdf_engine.rdf_store()
                    rdfs_store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load rdf from storage", e)
        self._load_file = False

    def reload(self, storage_factory, rdf_name):
        YLogger.debug(self, "Reloading RDF [%s]", rdf_name)
        self._load_file = True
        if storage_factory.entity_storage_engine_available(StorageFactory.RDF) is True:
            rdf_engine = storage_factory.entity_storage_engine(StorageFactory.RDF)
            if rdf_engine:
                try:
                    rdfs_store = rdf_engine.rdf_store()
                    rdfs_store.reload(self, rdf_name)
                except Exception as e:
                    YLogger.exception(self, "Failed to load rdf from storage", e)
        self._load_file = False

    def _write_updates(self, command, subject, predicate, obj):
        if self._load_file is True:
            return
        if self._storage_factory is None:
            return

        if self._storage_factory.entity_storage_engine_available(StorageFactory.RDF_UPDATES) is True:
            rdf_updates_engine = self._storage_factory.entity_storage_engine(StorageFactory.RDF_UPDATES)
            if rdf_updates_engine:
                try:
                    rdfs_updates_store = rdf_updates_engine.rdf_updates_store()
                    self._update_Date = datetime.now()
                    if command == 'add':
                        rdfs_updates_store.add_entry(subject, predicate, obj)
                    elif command == 'delete':
                        rdfs_updates_store.delete_entry(subject, predicate, obj)
                except Exception as e:
                    YLogger.exception(self, "Failed to Write rdf Updates", e)

    def subjects(self):
        return self._entities.keys()

    def predicates(self, subject):
        subject = self.convert_key(subject)
        if subject in self._entities:
            return self._entities[subject]._predicates.keys()
        return []

    def objects(self, subject, predicate):
        subject = self.convert_key(subject)
        if subject in self._entities:
            predicate = self.convert_key(predicate)
            if predicate in self._entities[subject]._predicates:
                return [self._entities[subject]._predicates[predicate]]
        return []

    def add_entity(self, subject, predicate, obj, rdf_name, rdf_store=None, id=None):
        YLogger.debug(self, "Adding RDF Entity [%s] [%s] [%s] [%s]", subject, predicate, obj, rdf_name)

        is_add = True
        subject = self.convert_key(subject)
        predicate = self.convert_key(predicate)
        obj = self.convert_key(obj)

        if subject not in self._entities:
            the_subject = RDFEntity(subject)
            self._entities[subject] = the_subject

            if id is not None:
                id = id.upper()
                if id not in self._entities_to_ids:
                    self._entities_to_ids[id] = []
                self._entities_to_ids[id].append(the_subject)

            self._stores[rdf_name] = rdf_store
            self._entities_to_stores[subject] = rdf_name

        entity = self._entities[subject]

        if predicate in entity._predicates:
            sub_entity = self._entities[subject]._predicates[predicate]
            if obj in sub_entity:
                is_add = False
            else:
                entity._predicates[predicate].append(obj)
        else:
            entity._predicates[predicate] = [obj]

        if is_add is True:
            self._write_updates('add', subject, predicate, obj)

    def has_subject(self, subject):
        subject = self.convert_key(subject)
        return bool(subject in self._entities)

    def has_predicate(self, subject, predicate):
        if self.has_subject(subject):
            predicate = self.convert_key(predicate)
            entity = self._entities[subject]

            return bool(predicate in entity._predicates)

        return False

    def has_object(self, subject, predicate, obj):
        if self.has_subject(subject):
            subject = self.convert_key(subject)
            entity = self._entities[subject]

            if self.has_predicate(subject, predicate):
                predicate = self.convert_key(predicate)
                objects = entity._predicates[predicate]

                obj = self.convert_key(obj)
                for object in objects:
                    if object == obj:
                        return True

        return False

    def delete_entity(self, subject, predicate=None, obj=None):
        YLogger.debug(self, "Deleting RDF Entity [%s] [%s] [%s]", subject, predicate, obj)
        subject = self.convert_key(subject)
        predicate = self.convert_key(predicate)
        obj = self.convert_key(obj)

        is_delete = False
        if self.has_subject(subject):

            if predicate is None and obj is None:
                YLogger.debug(None, "Removing entire subject %s", subject)
                del self._entities[subject]
                self._write_updates('delete', subject, predicate, obj)
                return

            entity = self._entities[subject]

            if obj is None:
                if self.has_predicate(subject, predicate):
                    YLogger.debug(None, "Removing entire predicate %s, subject %s", predicate, subject)
                    del entity._predicates[predicate]
                    is_delete = True
            else:
                if predicate in entity._predicates:
                    objects = entity._predicates[predicate]

                    if obj in objects:
                        YLogger.debug(None, "Removing object %s from predicate %s, subject %s", obj, predicate, subject)
                        objects = entity._predicates[predicate]
                        objects.remove(obj)
                        is_delete = True

                    if len(entity._predicates[predicate]) == 0:
                        YLogger.debug(None, "Removing empty predicate %s, subject %s", predicate, subject)
                        del entity._predicates[predicate]
                        is_delete = True

            if len(entity._predicates.keys()) == 0:
                YLogger.debug(None, "Removing empty subject %s", subject)
                del self._entities[subject]
                is_delete = True

        if is_delete is True:
            self._write_updates('delete', subject, predicate, obj)

    def all_as_tuples(self):
        all = []
        for subject, entity in self._entities.items():
            for predicate, objects in entity._predicates.items():
                for obj in objects:
                    all.append([subject, predicate, obj])
        return all

    def matched_as_tuples(self, subject=None, predicate=None, obj=None):
        YLogger.debug(self, "Matched tuple subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)
        subject = self.convert_key(subject)
        predicate = self.convert_key(predicate)
        obj = self.convert_key(obj)

        all = []
        for entity_subject, entity in self._entities.items():
            if subject is None or subject == entity_subject:
                for entity_predicate, entity_objects in entity._predicates.items():
                    if predicate is None or predicate == entity_predicate:
                        for entity_obj in entity_objects:
                            if obj is None or obj == entity_obj:
                                all.append([entity_subject, entity_predicate, entity_obj])
        return all

    def not_matched_as_tuples(self, subject=None, predicate=None, obj=None):
        YLogger.debug(self, "Matched tuple not subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)
        subject = self.convert_key(subject)
        predicate = self.convert_key(predicate)
        obj = self.convert_key(obj)

        all = []
        for entity_subject, entity in self._entities.items():
            if subject is None or subject == entity_subject:
                for entity_predicate, entity_objects in entity._predicates.items():
                    if predicate is None or predicate == entity_predicate:
                        for entity_obj in entity_objects:
                            if obj is not None and obj != entity_obj:
                                all.append([entity_subject, entity_predicate, entity_obj])
                    else:
                        for entity_obj in entity_objects:
                            all.append([entity_subject, entity_predicate, entity_obj])
            else:
                for entity_predicate, entity_objects in entity._predicates.items():
                    for entity_obj in entity_objects:
                        all.append([entity_subject, entity_predicate, entity_obj])

        return all

    def remove(self, entities, subject=None, predicate=None, obj=None):
        if predicate is None and obj is None:
            YLogger.debug(self, "Removing subject=[%s]", subject)
        elif obj is None:
            YLogger.debug(self, "Removing subject=[%s], predicate=[%s]", subject, predicate)
        else:
            YLogger.debug(self, "Removing subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)

        removes = []
        for entity in entities:
            if subject is not None:
                if predicate is not None:

                    if obj is not None:
                        if subject == entity[0] and predicate == entity[1] and obj == entity[2]:
                            removes.append(entity)

                    else:
                        if subject == entity[0] and predicate == entity[1]:
                            removes.append(entity)

                else:

                    if obj is not None:
                        if subject == entity[0] and obj == entity[2]:
                            removes.append(entity)

                    else:
                        if subject == entity[0]:
                            removes.append(entity)

            elif predicate is not None:

                if obj is not None:
                    if predicate == entity[1] and obj == entity[2]:
                        removes.append(entity)

                else:
                    if predicate == entity[1]:
                        removes.append(entity)

            elif obj is not None:

                if obj == entity[2]:
                    removes.append(entity)

        return [entity for entity in entities if entity not in removes]

    def _get_subject_element(self, subject, entity_subject):
        subj_element = None
        if subject is not None:

            if subject.startswith("?"):
                subj_element = [subject, entity_subject]

            elif subject == entity_subject:
                subj_element = ["subj", entity_subject]

        else:
            subj_element = ["subj", entity_subject]

        return subj_element

    def _get_predicate_element(self, predicate, entity_pred):
        pred_element = None
        if predicate is not None:

            if predicate.startswith("?"):
                pred_element = [predicate, entity_pred]

            elif predicate == entity_pred:
                pred_element = ["pred", entity_pred]

        else:
            pred_element = ["pred", entity_pred]

        return pred_element

    def _get_object_elements(self, entity, obj, entity_pred):

        obj_elements = []
        if obj is not None:

            if obj.startswith("?"):

                for object in entity._predicates[entity_pred]:
                    obj_elements.append([obj, object])

            else:

                for object in entity._predicates[entity_pred]:

                    if object == obj:
                        obj_elements.append(["obj", object])
        else:

            for object in entity._predicates[entity_pred]:
                obj_elements.append(["obj", object])

        return obj_elements

    def match_to_vars(self, subject=None, predicate=None, obj=None):
        YLogger.debug(self, "Matching subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)
        subject = self.convert_key(subject)
        predicate = self.convert_key(predicate)
        obj = self.convert_key(obj)

        results = []
        for entity_subject, entity in self._entities.items():
            subj_element = self._get_subject_element(subject, entity_subject)

            for entity_pred in entity._predicates:

                pred_element = self._get_predicate_element(predicate, entity_pred)

                obj_elements = self._get_object_elements(entity, obj, entity_pred)

                if subj_element is not None and pred_element is not None and len(obj_elements) > 0:
                    for object in obj_elements:
                        results.append([subj_element, pred_element, object])

        return results

    def not_match_to_vars(self, subject=None, predicate=None, obj=None):
        YLogger.debug(self, "Matching not subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)

        if subject is not None and subject.startswith("?") is True:
            all_subject = subject
        else:
            all_subject = None

        if predicate is not None and predicate.startswith("?") is True:
            all_predicate = predicate
        else:
            all_predicate = None

        if obj is not None and obj.startswith("?") is True:
            all_obj = obj
        else:
            all_obj = None

        all = self.match_to_vars(all_subject, all_predicate, all_obj)

        matched = self.match_to_vars(subject, predicate, obj)

        to_remove = []
        for entity in all:
            for atuple in matched:
                if entity[0][1] == atuple[0][1] and \
                   entity[1][1] == atuple[1][1] and \
                   entity[2][1] == atuple[2][1]:
                    to_remove.append(entity)

        return [entity for entity in all if entity not in to_remove]

    def match_only_vars(self, subject=None, predicate=None, obj=None):
        YLogger.debug(self, "Matching only vars subject=[%s], predicate=[%s], object=[%s]", subject, predicate, obj)

        results = self.match_to_vars(subject, predicate, obj)
        returns = []
        for atuple in results:
            aset = []
            for pair in atuple:
                if pair[0].startswith("?"):
                    aset.append(pair)
            if aset:
                returns.append(aset)

        return returns

    def get_unify_vars(self, vars):
        unified_vars = {}
        for var in vars:
            unified_vars[var] = None
        return unified_vars

    def dict_to_array(self, adict):
        atuple = []
        for name, value in adict.items():
            atuple.append([name, value])
        return atuple

    def unify(self, vars, sets):
        YLogger.debug(self, "Unifying Vars [%s]", vars)

        unifications = []
        if sets:
            # For each tuple in the first set
            for atuple in sets[0]:
                # Check to see if there are vars thay need unifying
                unified_vars = self.get_unify_vars(vars)
                if unified_vars:
                    # Get the value of the tuples which match the vars
                    if self.unify_tuple(atuple, unified_vars) is True:
                        # If we have more sets, keep checking that the vars are still matching
                        unified = True
                        if len(sets) > 1:
                            unified = self.unify_set(1, sets, unified_vars, 0)
                        # If we have unified all variables then we have a match
                        if unified is True:
                            result_vars = {}
                            for var_key, var_val in unified_vars.items():
                                if var_val is not None:
                                    result_vars[var_key] = var_val
                            if len(result_vars) > 0:
                                unifications.append(self.dict_to_array(result_vars))
                            else:
                                unifications.append(atuple)
        return unifications

    def unify_set(self, num_set, sets, unified_vars, depth):
        YLogger.debug(self, "Unifying Set")

        aset = sets[num_set]
        unified = False
        for atuple in aset:
            check_vars = unified_vars.copy()
            if 'match' in atuple:
                continue
            if self.unify_tuple(atuple, check_vars) is False:
                continue

            unified = True
            if num_set < len(sets)-1:
                unified = self.unify_set(num_set+1, sets, check_vars, depth+1)

            if unified is True:
                atuple.append('match')
                for key, val in check_vars.items():
                    if val is not None:
                        unified_vars[key] = val
                break

        return unified

    def unify_tuple(self, tuple, vars):
        YLogger.debug(self, "Unifying Tuple")

        for name, value in tuple:
            if name in vars:
                if vars[name] is None:
                    vars[name] = value
                else:
                    if vars[name] != value:
                        return False

        return True

    def apply_updates(self):
        YLogger.debug(self, "Apply RDF Updates Entity")
        if self._storage_factory.entity_storage_engine_available(StorageFactory.RDF_UPDATES) is True:
            rdf_updates_engine = self._storage_factory.entity_storage_engine(StorageFactory.RDF_UPDATES)
            if rdf_updates_engine:
                try:
                    rdfs_updates_store = rdf_updates_engine.rdf_updates_store()
                    self._load_file = True
                    rdfs_updates_store.apply_rdf_updates(self, self._update_Date)
                    self._update_Date = datetime.now()
                except Exception as e:
                    YLogger.exception(self, "Failed to Apply RDF Updates Entity", e)
        self._load_file = False

    def save_rdf_data(self):
        if len(self._entities) == 0:
            return
        YLogger.debug(self, "Save to File : RDF Entity")
        if self._storage_factory.entity_storage_engine_available(StorageFactory.RDF_UPDATES) is True:
            rdf_updates_engine = self._storage_factory.entity_storage_engine(StorageFactory.RDF_UPDATES)
            if rdf_updates_engine:
                try:
                    rdfs_updates_store = rdf_updates_engine.rdf_updates_store()
                    rdfs_updates_store.save_rdf_data(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to Save RDF Data", e)

    def convert_key(self, key_item):
        if key_item is not None:
            key_item = JapaneseLanguage.zenhan_normalize(key_item)
            if key_item.startswith("?") is False:
                key_item = key_item.upper()

        return key_item
