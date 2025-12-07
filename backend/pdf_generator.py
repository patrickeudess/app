"""
Générateur de rapports PDF pour Mon Cacao
"""
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from database import Database
import os
from io import BytesIO

class PDFGenerator:
    def __init__(self):
        self.db = Database()
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configurer les styles personnalisés"""
        # Style de titre
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2E8B57'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Style de sous-titre
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=20
        )
        
        # Style de texte normal
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12
        )
    
    def generate_professional_report(self, professional_id, output_path=None):
        """Générer un rapport professionnel complet"""
        if output_path is None:
            output_path = BytesIO()
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # En-tête
        story.append(Paragraph("Rapport Professionnel - Mon Cacao", self.title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.normal_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Récupérer les données
        producers = self.db.get_producers_by_professional(professional_id)
        submissions = self.db.get_submissions(professional_id=professional_id)
        stats = self.db.get_advice_stats(professional_id)
        
        # Statistiques globales
        story.append(Paragraph("Statistiques Globales", self.subtitle_style))
        
        total_production = sum(s.get('production_reelle', 0) or 0 for s in submissions)
        total_revenue = sum(s.get('revenu_total', 0) or 0 for s in submissions)
        total_submissions = len(submissions)
        
        stats_data = [
            ['Métrique', 'Valeur'],
            ['Nombre de producteurs', str(len(producers))],
            ['Soumissions totales', str(total_submissions)],
            ['Production totale (kg)', f"{total_production:,.0f}"],
            ['Revenus totaux (FCFA)', f"{total_revenue:,.0f}"],
            ['Conseils donnés', str(stats.get('total', 0))]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E8B57')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Liste des producteurs
        story.append(Paragraph("Liste des Producteurs", self.subtitle_style))
        
        if producers:
            producer_data = [['Nom', 'Région', 'Code', 'Soumissions']]
            for producer in producers:
                producer_submissions = [s for s in submissions if s.get('producer_id') == producer['id']]
                producer_data.append([
                    producer['name'],
                    producer.get('region', 'N/A'),
                    producer['code'],
                    str(len(producer_submissions))
                ])
            
            producer_table = Table(producer_data, colWidths=[2*inch, 1.5*inch, 2*inch, 1*inch])
            producer_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(producer_table)
        else:
            story.append(Paragraph("Aucun producteur enregistré", self.normal_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Analyse des conseils
        if stats.get('total', 0) > 0:
            story.append(Paragraph("Analyse des Conseils", self.subtitle_style))
            
            advice_data = [['Catégorie', 'Nombre']]
            for category, count in stats.get('by_category', {}).items():
                advice_data.append([category, str(count)])
            
            advice_table = Table(advice_data, colWidths=[3*inch, 2*inch])
            advice_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFD700')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(advice_table)
        
        # Pied de page
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            f"Généré par Mon Cacao - {datetime.now().strftime('%d/%m/%Y')}",
            ParagraphStyle('Footer', parent=self.styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
        ))
        
        # Générer le PDF
        doc.build(story)
        
        return output_path
    
    def generate_producer_report(self, producer_id, output_path=None):
        """Générer un rapport pour un producteur spécifique"""
        if output_path is None:
            output_path = BytesIO()
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Récupérer les données du producteur
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM producers WHERE id = ?', (producer_id,))
        producer = dict(cursor.fetchone())
        conn.close()
        
        submissions = self.db.get_submissions(producer_id=producer_id)
        
        # En-tête
        story.append(Paragraph(f"Rapport Producteur - {producer['name']}", self.title_style))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Code: {producer['code']}", self.normal_style))
        story.append(Paragraph(f"Région: {producer.get('region', 'N/A')}", self.normal_style))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", self.normal_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Statistiques du producteur
        story.append(Paragraph("Statistiques", self.subtitle_style))
        
        total_production = sum(s.get('production_reelle', 0) or 0 for s in submissions)
        total_revenue = sum(s.get('revenu_total', 0) or 0 for s in submissions)
        avg_production = total_production / len(submissions) if submissions else 0
        
        stats_data = [
            ['Métrique', 'Valeur'],
            ['Soumissions', str(len(submissions))],
            ['Production totale (kg)', f"{total_production:,.0f}"],
            ['Revenus totaux (FCFA)', f"{total_revenue:,.0f}"],
            ['Production moyenne (kg)', f"{avg_production:,.0f}"]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E8B57')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Historique des soumissions
        if submissions:
            story.append(Paragraph("Historique des Soumissions", self.subtitle_style))
            
            submission_data = [['Date', 'Production (kg)', 'Revenus (FCFA)']]
            for sub in submissions[:10]:  # Limiter à 10 dernières
                date_str = sub.get('date_soumission', '')[:10] if sub.get('date_soumission') else 'N/A'
                submission_data.append([
                    date_str,
                    f"{sub.get('production_reelle', 0) or 0:,.0f}",
                    f"{sub.get('revenu_total', 0) or 0:,.0f}"
                ])
            
            submission_table = Table(submission_data, colWidths=[2*inch, 2*inch, 2*inch])
            submission_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(submission_table)
        
        # Pied de page
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            f"Généré par Mon Cacao - {datetime.now().strftime('%d/%m/%Y')}",
            ParagraphStyle('Footer', parent=self.styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.grey)
        ))
        
        doc.build(story)
        
        return output_path

