from spacy import load
import networkx as nx
from typing import List, Dict, Tuple
import re
import json

class KnowledgeGraphBuilder:
    def __init__(self):
        self.nlp = load('en_core_web_sm')
        self.graph = nx.DiGraph()
        
    def extract_entities_relations(self, text: str) -> List[Tuple]:
        doc = self.nlp(text)
        relations = []
        
        for sent in doc.sents:
            # Get named entities and noun chunks
            entities = [(e.text, e.label_) for e in sent.ents]
            noun_chunks = [chunk.text for chunk in sent.noun_chunks]
            
            # Extract subject-verb-object triples
            for token in sent:
                if token.dep_ == "ROOT" or token.pos_ == "VERB":
                    subject = None
                    obj = None
                    
                    # Find subject
                    for child in token.children:
                        # Expanded subject detection
                        if child.dep_ in ["nsubj", "nsubjpass", "expl"]:
                            # Get the full noun phrase
                            subject = ' '.join([w.text for w in child.subtree])
                        # Expanded object detection
                        elif child.dep_ in ["dobj", "pobj", "attr", "acomp"]:
                            # Get the full noun phrase
                            obj = ' '.join([w.text for w in child.subtree])
                    
                    if subject and obj:
                        # Clean the terms
                        subject = subject.strip().lower()
                        obj = obj.strip().lower()
                        relation = token.text.strip().lower()
                        
                        # Add the relation
                        relations.append((subject, relation, obj))
                        
                        # Add inverse relation for better connectivity
                        relations.append((obj, f"is {relation} by", subject))
            
            # Add relationships between consecutive entities
            for i in range(len(entities)-1):
                e1, e2 = entities[i], entities[i+1]
                relations.append((e1[0].lower(), "related_to", e2[0].lower()))
            
            # Add relationships between noun chunks
            for i in range(len(noun_chunks)-1):
                n1, n2 = noun_chunks[i], noun_chunks[i+1]
                relations.append((n1.lower(), "associated_with", n2.lower()))
        
        return relations

    def build_graph(self, text: str):
        # Clean and preprocess text
        text = re.sub(r'\s+', ' ', text)
        relations = self.extract_entities_relations(text)
        
        # Build graph with weights
        for subj, pred, obj in relations:
            # Add nodes with type information
            self.graph.add_edge(
                subj, 
                obj, 
                relation=pred,
                weight=1.0  # Can be adjusted based on relationship confidence
            )
    
    def query_graph(self, query: str) -> str:
        """Extract relevant relationships from the knowledge graph."""
        doc = self.nlp(query)
        query_entities = [ent.text for ent in doc.ents]
        
        if not query_entities:
            # If no entities found, try using key terms
            query_terms = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
            query_entities = query_terms
        
        relevant_paths = []
        for entity in query_entities:
            if entity in self.graph:
                # Get direct relationships
                for neighbor in self.graph.neighbors(entity):
                    edge_data = self.graph[entity][neighbor]
                    relevant_paths.append(f"- {entity} {edge_data['relation']} {neighbor}")
                
                # Get 2-step relationships for all other nodes
                for target in self.graph.nodes():
                    if target != entity:
                        try:
                            paths = list(nx.all_simple_paths(self.graph, entity, target, cutoff=2))
                            for path in paths:
                                if len(path) > 1:
                                    path_desc = []
                                    for i in range(len(path)-1):
                                        edge_data = self.graph[path[i]][path[i+1]]
                                        path_desc.append(f"{path[i]} {edge_data['relation']} {path[i+1]}")
                                    relevant_paths.append(f"- {' -> '.join(path_desc)}")
                        except nx.NetworkXNoPath:
                            continue
        
        if relevant_paths:
            return "\n".join(relevant_paths)
        return "No direct relationships found in the knowledge graph."

    def get_graph_data(self, query: str = None) -> dict:
        """Return graph data in a format suitable for visualization"""
        if query:
            # Extract query entities and get relevant subgraph
            doc = self.nlp(query)
            query_entities = [ent.text for ent in doc.ents]
            relevant_nodes = set()
            
            for entity in query_entities:
                if entity in self.graph:
                    # Get neighbors within 2 steps
                    neighbors = nx.single_source_shortest_path(self.graph, entity, cutoff=2)
                    relevant_nodes.update(neighbors.keys())
            
            # Create subgraph
            subgraph = self.graph.subgraph(relevant_nodes)
        else:
            subgraph = self.graph

        # Convert to visualization format
        nodes = [{"id": node, "label": node} for node in subgraph.nodes()]
        edges = [
            {
                "source": u,
                "target": v,
                "label": d["relation"]
            }
            for u, v, d in subgraph.edges(data=True)
        ]
        
        return {"nodes": nodes, "edges": edges} 